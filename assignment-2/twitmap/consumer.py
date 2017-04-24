from kafka import KafkaConsumer
import boto3
import json

sns = boto3.client('sns')
arn = ''
consumer = KafkaConsumer('', bootstrap_servers="")
for message in consumer:
	all_data = json.loads(message.value)
	print(all_data)		
	response = sns.publish(
		TargetArn=arn,
		Message=json.dumps(all_data))
