from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
#consumer = KafkaConsumer('my-topic',
#                         group_id='my-group',
 #                        bootstrap_servers=['localhost:9092'])
consumer = KafkaConsumer('my-topic')
for message in consumer:
	print(message)