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

# app = Flask(__name__)

# KAFKA_GCP_BLOB_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_BLOB_RESPONSE_TOPIC") or 'gcp_blob_response'
# KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
# KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_OCR_FILE_TOPIC") or 'gcp_ocr'
# KAFKA_OCR_FILE_RESPONSE_TOPIC = os.getenv("KAFKA_OCR_FILE_RESPONSE_TOPIC") or 'gcp_ocr_response'

# producer = KafkaProducer(bootstrap_servers='localhost:9092', 
#    # value_serializer=lambda m: m.encode('utf-8'), 
#    key_serializer=lambda m: m.encode('utf-8')
#    )

# consumerBlobResponse = KafkaConsumer(KAFKA_GCP_BLOB_TOPIC, bootstrap_servers='localhost:9092',
#    value_deserializer=lambda m: json.loads(m.decode('ascii')))
   
# consumerOcrResponse = KafkaConsumer(KAFKA_OCR_FILE_TOPIC, bootstrap_servers='localhost:9092')

# def runConsumersBlobResponse():
#    for msg in consumerBlobResponse:
#       uuid = msg.key
#       print(uuid)
#       print("BLOB:",msg.value)
      
#       # res = json.loads(msg.value).decode('utf-8')
#       # if res['success']:
#       print("File uploaded to GCP bucket successfully")
#          # producer.send(topic=KAFKA_OCR_FILE_TOPIC, key=uuid, value='dummy message')
   
# def runConsumersOcrResponse():
#    for msg in consumerOcrResponse:
#       print("OCR:",json.loads(msg.value))
#       uuid = msg.key.decode('utf-8')
#       res = json.loads(msg.value).decode('utf-8')
#       if res['success']:
#          print("Image scanned using OCR successfully")


# runConsumersBlobResponse()




# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('gcp_blob_response',
                        #  group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

# consume earliest available messages, don't commit offsets
# KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
# KafkaConsumer()

# consume msgpack
# KafkaConsumer(value_deserializer=msgpack.unpackb)

# # StopIteration if no message after 1sec
# KafkaConsumer(consumer_timeout_ms=1000)

# # Subscribe to a regex topic pattern
# consumer = KafkaConsumer()
# consumer.subscribe(pattern='^awesome.*')

# # Use multiple consumers in parallel w/ 0.9 kafka brokers
# # typically you would run each on a different server / process / CPU
# consumer1 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')
# consumer2 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')