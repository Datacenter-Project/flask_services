from kafka import KafkaConsumer, KafkaProducer
import pickle
import os
import uuid
import json
import sys
import gcp_utils

from constants import *


producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST], 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii')
   )

consumer = KafkaConsumer(KAFKA_GCP_BLOB_TOPIC, 
# auto_offset_reset='earliest', 
bootstrap_servers=[KAFKA_HOST])

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    blob_name_uuid = msg.key.decode('utf-8')
    gcp_utils.upload_blob_from_string(BUCKET_NAME, msg.value, blob_name_uuid)      
    
    producer.send(topic='gcp_blob_response', 
        key=blob_name_uuid, 
        value={'success': True})

