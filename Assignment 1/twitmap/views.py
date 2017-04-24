from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys
import elasticsearch
from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
import geocoder
from django.views.decorators.csrf import csrf_protect



def index(request):
    return render(request, 'home.html')

def home(request):
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


		# import twitter keys and tokens

	# create instance of elasticsearch


	class TweetStreamListener(StreamListener):
		def __init__(self, time_limit=25):
			self.start_time = time.time()
			self.limit = time_limit

			# on success
		def on_data(self, data):
			# decode json
			all_data = json.loads(data)

			if (time.time() - self.start_time) < self.limit:
				if 'user' in all_data and all_data['user']['location']!='null':
					try:
						doc = {"username": all_data["user"]["screen_name"],
							   "latitude": geocoder.google(all_data['user']['location']).latlng[0],
							   "longitude": geocoder.google(all_data['user']['location']).latlng[1],
							   "tweetmessage": all_data["text"],
							   "my_id": query}
						es.index(index="collectedtweets",doc_type="tweets",body=doc)
					except:
						pass
					return True
			else:
				return False

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

	query = str(request.POST.get('myword'))

	stream.filter(track=['#'+query])

	pass_list = {}

	pass_list.setdefault('tweet', [])

	res = es.search(size=5000, index="collectedtweets", doc_type="tweets", body={
		"query":{
			"match" : { "my_id": query}
		}
	})

	for j in res['hits']['hits']:
		pass_list['tweet'].append(j['_source'])
		
	pass_list_final={}
	pass_list_final = json.dumps(pass_list)

	return render(request,"index.html",{"my_data":pass_list_final})


