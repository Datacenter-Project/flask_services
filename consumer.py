from kafka import KafkaConsumer
import json
# To consume latest messages and auto-commit offsets
# consumer = KafkaConsumer('json-topic',
#                         #  group_id='my-group',
#                          bootstrap_servers='localhost:9092')
# for message in consumer:
#     # message value and key are raw bytes -- decode if necessary!
#     # e.g., for unicode: `message.value.decode('utf-8')`
#     print ("%s:%d:%d: key=%s value=%s"  ( message.key,message.value))

# # consume earliest available messages, don't commit offsets
# KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# # consume json messages
consumer2 = KafkaConsumer('json-topic',
                        #  group_id=None,
                         bootstrap_servers='localhost:9092', 
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))
print(consumer2.bootstrap_connected())
print(consumer2.topics())
for message in consumer2:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print (message.key,message.value)

# # consume msgpack
# KafkaConsumer(value_deserializer=msgpack.unpackb)

# # StopIteration if no message after 1sec
# KafkaConsumer(consumer_timeout_ms=1000)

# # Subscribe to a regex topic pattern
# consumer = KafkaConsumer()
# consumer.subscribe(pattern='^awesome.*')

# # Use multiple consumers in parallel w/ 0.9 kafka brokers
# # typically you would run each on a different server / process / CPU
# consumer1 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')
# consumer2 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')

# consumer2.close()