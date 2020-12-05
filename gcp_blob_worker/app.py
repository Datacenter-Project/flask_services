from kafka import KafkaConsumer, KafkaProducer
import pickle
import gcp_utils
import os
import uuid
import json

KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME") or 'datacenter_project_bucket'

producer = KafkaProducer(bootstrap_servers='localhost:9092', 
   key_serializer=lambda m: m.encode('utf-8'),
   value_serializer=lambda m: json.dumps(m).encode('ascii')
   )

consumer = KafkaConsumer(KAFKA_GCP_BLOB_TOPIC, bootstrap_servers='localhost:9092')

for msg in consumer:
    print('Message key:', msg.key.decode('utf-8'))
    blob_name_uuid = msg.key.decode('utf-8')
    gcp_utils.upload_blob_from_string(BUCKET_NAME, msg.value, blob_name_uuid)      
    
    producer.send(topic='gcp_blob_response', 
        key=blob_name_uuid, 
        value={'success': True})

