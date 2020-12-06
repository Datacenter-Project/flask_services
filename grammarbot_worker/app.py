from urllib import quote
import requests
import json
from kafka import KafkaConsumer, KafkaProducer
import os
from elasticsearch import Elasticsearch
import json
from flask import jsonify
from bson import json_util
KAFKA_GRAMMAR_BOT_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_FILE_TOPIC") or 'gcp_grammar_bot'
KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC") or 'gcp_grammar_bot_response'
ES_HOST = os.getenv("ES_HOST") or 'localhost'
ES_PORT = os.getenv("ES_PORT") or '9200'
ES_INDEX = 'ocr_texts'

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}]    
)
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii'))

consumer = KafkaConsumer(KAFKA_GRAMMAR_BOT_TOPIC, bootstrap_servers='localhost:9092')

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    uuid = msg.key.decode('utf-8')

    body = {
        "query": {
            "multi_match": {
                "query": uuid,
                "fields": ["uuid"]
            }
        }
    }

    res = es.search(index=ES_INDEX, body=body)

    text = quote(res['hits']['hits'][0]['_source']['ocr_text'])
    url = "https://grammarbot.p.rapidapi.com/check"
    payload = "text=" + text + "&language=en-US"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "14c63f9d86msh74179affcc45362p13eb62jsn91cf19c77826",
        'x-rapidapi-host': "grammarbot.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(json.loads(response.text)["matches"])
    producer.send(topic=KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC, 
        key=uuid, 
        value=json.loads(response.text)["matches"])
        

      

