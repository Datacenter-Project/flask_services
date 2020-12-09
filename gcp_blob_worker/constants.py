import os

# KAFKA_GCP_BLOB_RESPONSE_TOPIC = 'gcp_blob_response'
# KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
# KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_IMAGE_FILE_TOPIC") or 'gcp_ocr'
# ES_HOST = os.getenv("ES_HOST") or 'localhost'
# ES_PORT = os.getenv("ES_PORT") or '443'
# ES_INDEX = ''

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME") or 'datacenter_project_bucket'

KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'

KAFKA_GCP_BLOB_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_BLOB_RESPONSE_TOPIC") or 'gcp_blob_response'

KAFKA_HOST = os.getenv("KAFKA_HOST") or 'localhost:9092'
