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
import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import *
from google.cloud import logging

app = Flask(__name__)

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)


producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST], 
   # value_serializer=lambda m: m.encode('utf-8'), 
   key_serializer=lambda m: m.encode('utf-8')
)

consumerBlobResponse = KafkaConsumer(KAFKA_GCP_BLOB_RESPONSE_TOPIC,                        
                        bootstrap_servers=[KAFKA_HOST],
                        value_deserializer=lambda m: json.loads(m.decode('ascii')))

consumerOcrResponse = KafkaConsumer(KAFKA_GCP_OCR_RESPONSE_TOPIC, 
                        bootstrap_servers=[KAFKA_HOST],
                        value_deserializer=lambda m: json.loads(m.decode('ascii')))

consumerGrammarbotResponse = KafkaConsumer(KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC, 
                        bootstrap_servers=[KAFKA_HOST])

consumerSearchResponse = KafkaConsumer(KAFKA_SEARCH_RESPONSE_TOPIC, 
                        bootstrap_servers=[KAFKA_HOST])

logging_client = logging.Client()
# logger = logging_client.logger(LOGGER_NAME)
logging_client.get_default_handler()
logging_client.setup_logging()

import logging

logging.basicConfig(filename='temp.log', filemode='w', format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)


# # [START logging_write_log_entry]
# def write_entry(logger_name):
#     """Writes log entries to the given logger."""
    

#     # This log can be found in the Cloud Logging console under 'Custom Logs'

#     # Make a simple text log
#     logger.log_text("Hello, world! - new")

#     # Simple text log with severity.
#     logger.log_text("Goodbye, world!", severity="ERROR")

#     # Struct log. The struct can be any JSON-serializable dictionary.
#     logger.log_struct(
#         {
#             "name": "King Arthur",
#             "quest": "Find the Holy Grail",
#             "favorite_color": "Blue",
#         }
#     )

#     print("Wrote logs to {}.".format(logger.name))

def runConsumersBlobResponse():

   logging.info("Starting consumer for GCP blob worker response")

   # consumer = KafkaConsumer('gcp_blob_response',
   #                      #  group_id='my-group',
   #                       bootstrap_servers=[KAFKA_HOST],
   #                       value_deserializer=lambda m: json.loads(m.decode('ascii')))
   for msg in consumerBlobResponse:
      # message value and key are raw bytes -- decode if necessary!
      # e.g., for unicode: `msg.value.decode('utf-8')`
      logging.info("Received a new message in GCP blob response consumer")

      print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value))
      uuid = msg.key
      if msg.value['success']:
         print("File uploaded to GCP bucket successfully")
         logging.info("File uploaded to GCP bucket successfully")
         # producer.send(topic=KAFKA_OCR_FILE_TOPIC, key=uuid, value='dummy message')
   
def runConsumersOcrResponse():
   logging.info("Starting consumer for OCR worker response")

   for msg in consumerOcrResponse:     
      print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value)) 
      logging.info("Received a new message in OCR response consumer")
      
      uuid = msg.key      
      if msg.value['success']:
         print("Image scanned using OCR successfully")
         logging.info("Image scanned using OCR successfully")

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
   logging.info("Received a request for /upload endpoint")
   try:
      f = request.files['file']
      blob_name_uuid = str(uuid.uuid4())
      fin = f.stream.read()      
      filename = secure_filename(f.filename)
      print("filename:", filename)

      producer.send(topic=KAFKA_GCP_BLOB_TOPIC, value=fin, key=blob_name_uuid)
      logging.info("Sent a message to GCP blob worker")
      print("Sent message to GCP blob worker")
      # .add_callback(on_blob_success)

      # def on_ocr_success():
      #    pass

      # def on_blob_success():
      producer.send(topic=KAFKA_OCR_FILE_TOPIC, value=fin, key=blob_name_uuid)
      logging.info("Sent a message to OCR worker")
      print("Sent message to OCR worker")
      # .add_callback(on_ocr_success)
      
     
      response = {
         'success': True,
         # 'message': 'Image read and scanned successfully'
      }
      logging.info("Sent response back to the client")
      return Response(response=json.dumps(response), status=200) 
   except Exception as e:
      print("Something wrong occurred")
      print(e)
      logging.error("Something wrong occurred - "+str(e))
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)

@app.route("/grammar/<uuid>", methods=['GET'])
def grammar_check(uuid):

   try:
      # if 'uuid' in request.args:
      #    uuid = request.args.get('uuid')
      producer.send(topic=KAFKA_GRAMMAR_BOT_TOPIC, key=uuid)
      for msg in consumerGrammarbotResponse:
         return Response(response=msg.value, status=200)
      
   except Exception as e:
      print('Something wrong occurred')
      print(e)
      logging.error("Something wrong occurred - "+str(e))
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)

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

   except Exception as e:
      print('Something wrong occurred')
      print(e)
      logging.error("Something wrong occurred - "+str(e))

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
      print("Something wrong occurred")
      print(e)
      logging.error("Something wrong occurred - "+str(e))
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
      print("Something wrong occurred")
      print(e)
      logging.error("Something wrong occurred - "+str(e))
      return Response(response=json.dumps({'success':False, 'message':'Something wrong occurred'}), status=500)

if __name__ == '__main__':
   # write_entry('my-logs')   
   thread1 = Thread(target = runConsumersBlobResponse, daemon=True)
   thread1.start()
   thread2 = Thread(target = runConsumersOcrResponse, daemon=True)
   thread2.start()
   app.run(debug = True, host='0.0.0.0', port=5010)

   # print(constants.KAFKA_GCP_BLOB_RESPONSE_TOPIC)