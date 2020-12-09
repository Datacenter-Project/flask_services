from kafka import KafkaConsumer, KafkaProducer
import pickle
import gcp_utils
import os
from elasticsearch import Elasticsearch
import json
import sys
from constants import *

es = Elasticsearch(
    # hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)

from google.cloud import logging

logging_client = logging.Client()
# logger = logging_client.logger(LOGGER_NAME)
logging_client.get_default_handler()
logging_client.setup_logging()

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)


producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii'))
# print("KAFKA_OCR_FILE_TOPIC", KAFKA_OCR_FILE_TOPIC)
consumer = KafkaConsumer(KAFKA_OCR_FILE_TOPIC, 
# auto_offset_reset='earliest', 
bootstrap_servers=KAFKA_HOST)

for msg in consumer:
    logging.info("Received a new message in "+str(KAFKA_OCR_FILE_TOPIC)+" topic in OCR worker")
    print('Message key:', msg.key.decode('utf-8'))
    uuid = msg.key.decode('utf-8')

    logging.info("Processing the image to extract OCR")

    texts = gcp_utils.detect_document_from_file(msg.value)

    doc = {
        'uuid': uuid,
        'ocr_text': texts[0]
    }

    logging.info("Adding the extracted OCR text to Elasticsearch")

    res = es.index(index=ES_INDEX, body=doc, refresh=True)

    logging.info('Sending the message acknowledgement in the OCR worker')
    producer.send(topic=KAFKA_GCP_OCR_RESPONSE_TOPIC, 
        key=uuid, 
        value={'success': True})
