from kafka import KafkaProducer
from kafka.errors import KafkaError
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sys

	#producer = KafkaProducer(bootstrap_servers=['broker1:1234'])
producer = KafkaProducer()

	# Asynchronous by default
	# future = producer.send('my-topic', b'raw_bytes')
ckey="CaeDRzSdQwKX3Zq2wRkRtDEiA"
csecret="IdECz0Bb4BWDs78TUAKqOkHT84HXf3dQ4XkHpEpeilF2I2Ai2v"
atoken="4812013898-qG0lcqL1xAzI9yZN9wP5tn4CYpRyN8LruXG1se9"
asecret="6jiXY4om2ZIjbslirBRp2X4XXVccDRuGYe0XOHWRMhT6N"
		# host = 'search-priyanshi-35mcs4sifteslgsqi5i7zvfzpi.us-west-2.es.amazonaws.com'
		# awsauth = AWS4Auth('AKIAIUZTNXEADE7NAXMA', '/mr9JoWqvG86xR5jF5gaVwXfA6GRkBljeFwfkCr5', 'us-west-2', 'es')
		# # 	es = elasticsearch.Elasticsearch(
		# 	hosts=[{'host': host, 'port': 443}],
		# 	http_auth=awsauth,
		# 	use_ssl=True,
		# 	verify_certs=True,
		# 	connection_class=elasticsearch.connection.RequestsHttpConnection
		# )


			# import twitter keys and tokens

		# create instance of elasticsearch


class TweetStreamListener(StreamListener):
			# def __init__(self, time_limit=25):
			# 	self.start_time = time.time()
			# 	self.limit = time_limit

				# on success
	def on_data(self, data):
				# decode json
		all_data = json.loads(data)

	# 			if (time.time() - self.start_time) < self.limit:
		if 'user' in all_data and all_data['user']['location']!='null':
			future = producer.send('my-topic', 'all_data')
						# try:
						# 	doc = {"username": all_data["user"]["screen_name"],
						# 		   "latitude": geocoder.google(all_data['user']['location']).latlng[0],
						# 		   "longitude": geocoder.google(all_data['user']['location']).latlng[1],
						# 		   "tweetmessage": all_data["text"],
						# 		   "my_id": query}
						# 	es.index(index="collectedtweets",doc_type="tweets",body=doc)
				# 		# except:
				# 			pass
				# 		return True
				# else:
				# 	return False

					# on failure

	def on_error(self, status):
		print(status)


		# create instance of the tweepy tweet stream listener
	listener = TweetStreamListener()

		# set twitter keys/tokens
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

		# create instance of the tweepy stream
	stream = Stream(auth, listener)

	stream.filter(track=['#'+query])
