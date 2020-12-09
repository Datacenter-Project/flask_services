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
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii'))
print("KAFKA_OCR_FILE_TOPIC", KAFKA_OCR_FILE_TOPIC)
consumer = KafkaConsumer(KAFKA_OCR_FILE_TOPIC, 
# auto_offset_reset='earliest', 
bootstrap_servers=KAFKA_HOST)

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    uuid = msg.key.decode('utf-8')
    texts = gcp_utils.detect_document_from_file(msg.value)

    doc = {
        'uuid': uuid,
        'ocr_text': texts[0]
    }

    res = es.index(index=ES_INDEX, body=doc, refresh=True)

    producer.send(topic=KAFKA_GCP_OCR_RESPONSE_TOPIC, 
        key=uuid, 
        value={'success': True})
