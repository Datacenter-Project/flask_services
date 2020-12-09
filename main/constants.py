import os

# KAFKA_GCP_BLOB_RESPONSE_TOPIC = 'gcp_blob_response'
# KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
# KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_IMAGE_FILE_TOPIC") or 'gcp_ocr'
# ES_HOST = os.getenv("ES_HOST") or 'localhost'
# ES_PORT = os.getenv("ES_PORT") or '443'
# ES_INDEX = ''

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME") or 'datacenter_project_bucket'

KAFKA_GCP_BLOB_TOPIC = os.getenv("KAFKA_GCP_BLOB_TOPIC") or 'gcp_blob'
KAFKA_OCR_FILE_TOPIC = os.getenv("KAFKA_OCR_FILE_TOPIC") or 'gcp_ocr'
KAFKA_GRAMMAR_BOT_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_FILE_TOPIC") or 'gcp_grammar_bot'
KAFKA_SEARCH_TOPIC = os.getenv("KAFKA_SEARCH_FILE_TOPIC") or 'gcp_search'

KAFKA_GCP_BLOB_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_BLOB_RESPONSE_TOPIC") or 'gcp_blob_response'
KAFKA_GCP_OCR_RESPONSE_TOPIC = os.getenv("KAFKA_GCP_OCR_RESPONSE_TOPIC") or 'gcp_ocr_response'
KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC = os.getenv("KAFKA_GRAMMAR_BOT_RESPONSE_TOPIC") or 'gcp_grammar_bot_response'
KAFKA_SEARCH_RESPONSE_TOPIC = os.getenv("KAFKA_SEARCH_RESPONSE_TOPIC") or 'gcp_search_response'

ES_HOST = os.getenv("ES_HOST") or 'localhost'
ES_PORT = os.getenv("ES_PORT") or '9200'
ES_INDEX = os.getenv("ES_INDEX") or 'ocr_texts'

KAFKA_HOST = os.getenv("KAFKA_HOST") or 'localhost:9092'

LOGGER_NAME = os.getenv('LOGGER_NAME') or 'main_service_logs'
