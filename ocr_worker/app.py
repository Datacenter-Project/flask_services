from kafka import KafkaConsumer, KafkaProducer
import pickle
import gcp_utils
import os
from elasticsearch import Elasticsearch
import json

KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_IMAGE_FILE_TOPIC") or 'gcp_ocr'
ES_HOST = os.getenv("ES_HOST") or 'localhost'
ES_PORT = os.getenv("ES_PORT") or '443'
ES_INDEX = 'ocr_texts'

es = Elasticsearch(
    # hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii'))

consumer = KafkaConsumer(KAFKA_OCR_FILE_TOPIC, bootstrap_servers='localhost:9092')

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    uuid = msg.key.decode('utf-8')
    texts = gcp_utils.detect_document_from_file(msg.value)

    doc = {
        'uuid': uuid,
        'ocr_text': texts[0]
    }

    res = es.index(index=ES_INDEX, body=doc, refresh=True)
    
    # es.indices.refresh(index="test-index")

    # producer.send(topic='gcp_blob_response', 
    #     key=json.dumps({'uuid': uuid}), 
    #     value=json.dumps({'success': True}))

    producer.send(topic='gcp_ocr_response', 
        key=uuid, 
        value={'success': True})

      

