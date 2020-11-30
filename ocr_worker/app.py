from kafka import KafkaConsumer
consumer = KafkaConsumer('foobar',bootstrap_servers='localhost:9092')
for msg in consumer:
    for line in msg:
        print(line)


