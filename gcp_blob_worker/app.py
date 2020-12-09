from kafka import KafkaConsumer, KafkaProducer
import pickle
import os
import uuid
import json
import sys
import gcp_utils

from constants import *


from google.cloud import logging

logging_client = logging.Client()
# logger = logging_client.logger(LOGGER_NAME)
logging_client.get_default_handler()
logging_client.setup_logging()

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)


producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST], 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii')
   )

consumer = KafkaConsumer(KAFKA_GCP_BLOB_TOPIC, 
# auto_offset_reset='earliest', 
bootstrap_servers=[KAFKA_HOST])

for msg in consumer:
    logging.info("Received a new message in "+str(KAFKA_GCP_BLOB_TOPIC)+" topic in the GCP blob worker")

    print('Message key:', msg.key.decode('utf-8'))
    blob_name_uuid = msg.key.decode('utf-8')
    logging.info("Uploading the image to GCP bucket "+str(BUCKET_NAME))

    gcp_utils.upload_blob_from_string(BUCKET_NAME, msg.value, blob_name_uuid)  

    logging.info('Sending the message acknowledgement from the GCP blob worker')
    
    producer.send(topic='gcp_blob_response', 
        key=blob_name_uuid, 
        value={'success': True})

