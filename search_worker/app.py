from urllib import quote
import requests
import json
from kafka import KafkaConsumer, KafkaProducer
import os
from elasticsearch import Elasticsearch
import json
from flask import jsonify
from bson import json_util
KAFKA_SEARCH_TOPIC = os.getenv("KAFKA_SEARCH_FILE_TOPIC") or 'gcp_search'
KAFKA_SEARCH_RESPONSE_TOPIC = os.getenv("KAFKA_SEARCH_RESPONSE_TOPIC") or 'gcp_search_response'
ES_HOST = os.getenv("ES_HOST") or 'localhost'
ES_PORT = os.getenv("ES_PORT") or '9200'
ES_INDEX = 'ocr_texts'

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii'))

consumer = KafkaConsumer(KAFKA_SEARCH_TOPIC, bootstrap_servers='localhost:9092')

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    uuid = msg.key.decode('utf-8')
    search_text = msg.value
    body = {
        "query": {
            "multi_match": {
                "query": search_text,
                "fields": ["ocr_text"]
            }
        }
    }

    res = es.search(index=ES_INDEX, body=body)

    print(res['hits']['hits'])
    producer.send(topic=KAFKA_SEARCH_RESPONSE_TOPIC, 
        key=uuid, 
        value=json.loads(res['hits']['hits']))