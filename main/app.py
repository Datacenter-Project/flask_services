from flask import Flask, render_template, request, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
# import gcp_utils
import uuid
from kafka import KafkaProducer, KafkaConsumer
import pickle
import json
import os
from threading import Thread
from elasticsearch import Elasticsearch
import gcp_utils
# from google.appengine.api import app_identity
# import cloudstorage
from flask import send_file

app = Flask(__name__)

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME") or 'datacenter_project_bucket'
KAFKA_GCP_BLOB_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_BLOB_RESPONSE_TOPIC") or 'gcp_blob_response'
KAFKA_OCR_FILE_RESPONSE_TOPIC = os.getenv("KAFKA_OCR_FILE_RESPONSE_TOPIC") or 'gcp_ocr_response'
KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC") or 'gcp_grammar_bot_response'
KAFKA_SEARCH_RESPONSE_TOPIC = os.getenv("KAFKA_SEARCH_RESPONSE_TOPIC") or 'gcp_search_response'

KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_OCR_FILE_TOPIC") or 'gcp_ocr'
KAFKA_GRAMMAR_BOT_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_FILE_TOPIC") or 'gcp_grammar_bot'
KAFKA_SEARCH_TOPIC = os.getenv("KAFKA_SEARCH_FILE_TOPIC") or 'gcp_search'

ES_HOST = os.getenv("ES_HOST") or 'localhost'
ES_PORT = os.getenv("ES_PORT") or '9200'
ES_INDEX = 'ocr_texts'

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)


producer = KafkaProducer(bootstrap_servers='localhost:9092', 
   # value_serializer=lambda m: m.encode('utf-8'), 
   key_serializer=lambda m: m.encode('utf-8')
)

consumerBlobResponse = KafkaConsumer(KAFKA_GCP_BLOB_RESPONSE_TOPIC,                        
                        bootstrap_servers=['localhost:9092'],
                        value_deserializer=lambda m: json.loads(m.decode('ascii')))

consumerOcrResponse = KafkaConsumer(KAFKA_OCR_FILE_RESPONSE_TOPIC, 
                        bootstrap_servers='localhost:9092',
                        value_deserializer=lambda m: json.loads(m.decode('ascii')))

consumerGrammarbotResponse = KafkaConsumer(KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC, 
                        bootstrap_servers='localhost:9092')

consumerSearchResponse = KafkaConsumer(KAFKA_SEARCH_RESPONSE_TOPIC, 
                        bootstrap_servers='localhost:9092')

def runConsumersBlobResponse():

   # consumer = KafkaConsumer('gcp_blob_response',
   #                      #  group_id='my-group',
   #                       bootstrap_servers=['localhost:9092'],
   #                       value_deserializer=lambda m: json.loads(m.decode('ascii')))
   for msg in consumerBlobResponse:
      # message value and key are raw bytes -- decode if necessary!
      # e.g., for unicode: `msg.value.decode('utf-8')`
      print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value))
      uuid = msg.key
      if msg.value['success']:
         print("File uploaded to GCP bucket successfully")
         # producer.send(topic=KAFKA_OCR_FILE_TOPIC, key=uuid, value='dummy message')
   
def runConsumersOcrResponse():
   for msg in consumerOcrResponse:     
      print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value)) 
      uuid = msg.key      
      if msg.value['success']:
         print("Image scanned using OCR successfully")

# def runConsumersGrammarbotResponse():
#    for msg in consumerGrammarbotResponse:     
#       print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
#                                              msg.offset, msg.key,
#                                              msg.value)) 
#       uuid = msg.key      
#       if msg.value['success']:
#          print("Grammar check successful")

@app.route('/upload', methods = ['POST'])
def upload_file():
   try:
      f = request.files['file']
      blob_name_uuid = str(uuid.uuid4())
      fin = f.stream.read()      
      filename = secure_filename(f.filename)
      print("filename:", filename)

      producer.send(topic=KAFKA_GCP_BLOB_TOPIC, value=fin, key=blob_name_uuid)
      print("Sent message to GCP blob worker")
      # .add_callback(on_blob_success)

      # def on_ocr_success():
      #    pass

      # def on_blob_success():
      producer.send(topic=KAFKA_OCR_FILE_TOPIC, value=fin, key=blob_name_uuid)
      print("Sent message to OCR worker")
      # .add_callback(on_ocr_success)
      
     
      response = {
         'success': True,
         # 'message': 'Image read and scanned successfully'
      }

      return Response(response=json.dumps(response), status=200) 
   except:
      print("Something wrong occurred")

@app.route("/grammar/<uuid>", methods=['GET'])
def grammar_check(uuid):

   try:
      # if 'uuid' in request.args:
      #    uuid = request.args.get('uuid')
      producer.send(topic=KAFKA_GRAMMAR_BOT_TOPIC, key=uuid)
      for msg in consumerGrammarbotResponse:
         return Response(response=msg.value, status=200)
      
   except:
      print('Something wrong occurred')

@app.route("/search", methods=['GET'])
def search():
   try:      
      if 'text' in request.args:
         # uuid = str(uuid.uuid4())
         text = request.args.get('text')
         # producer.send(topic=KAFKA_SEARCH_TOPIC, value=text, key=uuid)
         # for msg in consumerSearchResponse:
         #    return Response(response=msg.value, status=200)      

         body = {
            "query": {
                  "multi_match": {
                     "query": text,
                     "fields": ["ocr_text"]
                  }
            }
         }

         res = es.search(index=ES_INDEX, body=body)

         print(res['hits']['hits'])
         return Response(response=json.dumps(res['hits']['hits']), status=200)      

   except:
      print('Something wrong occurred')
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)
		
@app.route("/getDocs", methods=['GET'])
def getDocs():
   try:     
      # print(request.args) 
      start = 0
      size = 0
      if 'start' in request.args:         
         start = int(request.args.get('start'))
      if 'size' in request.args:         
         size = int(request.args.get('size'))
      # print(start, size)
      body = {
         "from": start,
         "size": size,
         "query": {
            "match_all": {}
         }
      }

      res = es.search(index=ES_INDEX, body=body)

      # print(res['hits']['hits'])
      return Response(response=json.dumps(res['hits']['hits']), status=200)      

   except Exception as e:
      print('Something wrong occurred')
      print(e)
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)
		
   
@app.route("/getImage", methods=['GET'])
def getImage():
   print(request.args)
   try:
      if 'uuid' in request.args:
         image_uuid = request.args.get('uuid')
         gcp_utils.download_blob(BUCKET_NAME, image_uuid, 'main/temp.png')
         # f_out = open('main/temp.png')
         return send_file('temp.png', mimetype='image/gif')
   except Exception as e:
      print('Something wrong occurred', e)
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)


if __name__ == '__main__':
   thread1 = Thread(target = runConsumersBlobResponse, daemon=True)
   thread1.start()
   thread2 = Thread(target = runConsumersOcrResponse, daemon=True)
   thread2.start()
   app.run(debug = True, host='0.0.0.0', port=5000)

   # print(constants.KAFKA_GCP_BLOB_RESPONSE_TOPIC)