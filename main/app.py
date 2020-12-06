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

# from .. import constants

app = Flask(__name__)

KAFKA_GCP_BLOB_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_BLOB_RESPONSE_TOPIC") or 'gcp_blob_response'
KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_OCR_FILE_TOPIC") or 'gcp_ocr'
KAFKA_OCR_FILE_RESPONSE_TOPIC = os.getenv("KAFKA_OCR_FILE_RESPONSE_TOPIC") or 'gcp_ocr_response'

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

@app.route('/upload', methods = ['POST'])
def upload_file():
   try:
      destination_blob_name = str(uuid.uuid4())
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
		
if __name__ == '__main__':
   thread1 = Thread(target = runConsumersBlobResponse, daemon=True)
   thread1.start()
   thread2 = Thread(target = runConsumersOcrResponse, daemon=True)
   thread2.start()
   app.run(debug = True, host='0.0.0.0', port=5000)
   # print(constants.KAFKA_GCP_BLOB_RESPONSE_TOPIC)