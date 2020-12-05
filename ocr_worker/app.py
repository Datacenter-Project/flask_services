from kafka import KafkaConsumer
import pickle
import gcp_utils

consumer = KafkaConsumer('foobar',bootstrap_servers='localhost:9092')

for msg in consumer:
    print(msg.key.decode('utf-8'))
    gcp_utils.detect_document_from_file(msg.value)
    # msg_2 = pickle.load(msg.value)
    # for line in msg_2:
    #     print(line)


