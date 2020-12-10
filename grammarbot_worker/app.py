from urllib.parse import quote
import requests
import json
from kafka import KafkaConsumer, KafkaProducer
import os
from elasticsearch import Elasticsearch
import json
# from flask import jsonify
# from bson import json_util
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

from google.cloud import logging

logging_client = logging.Client()
# logger = logging_client.logger(LOGGER_NAME)
logging_client.get_default_handler()
logging_client.setup_logging()

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

for msg in consumer:
    logging.info("Received a new message in "+str(KAFKA_GRAMMAR_BOT_TOPIC)+" topic in grammarbot worker")

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
    logging.info('Getting the OCR text for the document from Elasticsearch')
    res = es.search(index=ES_INDEX, body=body)

    text = quote(res['hits']['hits'][0]['_source']['ocr_text'])
    url = "https://grammarbot.p.rapidapi.com/check"
    payload = "text=" + text + "&language=en-US"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "grammarbot.p.rapidapi.com"
    }

    logging.info('Sending request to Grammarbot')
    logging.info('Request body '+json.dumps(payload))
    response = requests.request("POST", url, data=payload, headers=headers)
    # print(json.loads(response.text)["matches"])

    logging.info('Sending the message acknowledgement with the response body of the Grammarbot worker')

    producer.send(topic=KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC, 
        key=uuid, 
        value=json.loads(response.text)["matches"])
        

      

