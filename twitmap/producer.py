from kafka import KafkaProducer
from kafka.errors import KafkaError
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sys
from requests_aws4auth import AWS4Auth
# from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
import time
import elasticsearch
from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
import geocoder
from textblob import TextBlob
# from django.http import HttpResponse
from urllib2 import urlopen, HTTPError
from geopy.geocoders import Nominatim

producer = KafkaProducer(bootstrap_servers="172.31.44.184:9092",value_serializer=lambda v: json.dumps(v).encode('utf-8'))

ckey=""
csecret=""
atoken=""
asecret=""
host = ''
awsauth = AWS4Auth('', '', 'us-west-2', 'es')
es = elasticsearch.Elasticsearch(
	hosts=[{'host': host, 'port': 443}],
	http_auth=awsauth,
	use_ssl=True,
	verify_certs=True,
	connection_class=elasticsearch.connection.RequestsHttpConnection
)

class TweetStreamListener(StreamListener):
	def on_data(self, data):
		all_data = json.loads(data)
		geolocator = Nominatim()
		
		if 'user' in all_data and all_data['user']['location']!='null':
			try:
				location=geolocator.geocode(all_data['user']['location'])
				sent = TextBlob(all_data['text'])
				a = sent.sentiment.polarity
				if a > 0.25:
					senti = 'positive'
				elif a < -0.25:
					senti = 'negative'
				else:
					senti = 'neutral'

				doc = {"username": all_data["user"]["screen_name"],
						"lat": location.latitude,
						"lng": location.longitude,
						"tweetmessage": all_data["text"],
						"sentiment": senti
						}
				producer.send('my-topic', json.dumps(doc))
			except:
				pass
			return True
		else:
			return False

		def on_error(self, status):
			print(status)


listener = TweetStreamListener()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

stream = Stream(auth, listener)

stream.filter(track=['trump','mondaymotivation','FoodCity500','President Obama','Confederate'])
