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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib2 import urlopen, HTTPError

@csrf_exempt
def snsnotif(request):
    if request.method=="GET":
        context = {"title":"Home"}
        #return render(request, "index.html", context)
        return HttpResponse(status=200)
    else:
        headers = json.loads(request.body.decode("utf-8"))
        print("Serving SNS POST Request")
        if 'Type' in headers.keys():
            if headers['Type']=="SubscriptionConfirmation":
                print("Received Confirmation Request")
                subscribeUrl = headers['SubscribeURL']
                responseData = urlopen(subscribeUrl).read()
                print("Subscribed to SNS")
            elif headers['Type']=="Notification":
            	print ("Received a new message: "+str(headers["Message"]))
                message = json.loads(headers["Message"])
                print ("Message :"+str(message))
                
                host = ''
                awsauth = AWS4Auth('', '', 'us-west-2', 'es')
                es = elasticsearch.Elasticsearch(
                	hosts=[{'host': host, 'port': 443}],
                	http_auth=awsauth,
                	use_ssl=True,
                	verify_certs=True,
                	connection_class=elasticsearch.connection.RequestsHttpConnection
                )
                es.index(
                	index="collectedtweets",
                	doc_type="tweets",
                	body=message
                )
                #new_tweet = NewTweets(id=id, tweet=tweet, lat=lat, lng=lng, sentiment=sentiment)
                #new_tweet.save()
    	#return render(request, "home.html", {"post_params": str(request.POST)})
    	return HttpResponse(status=200)

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


	query = str(request.POST.get('myword'))

	# stream.filter(track=['#'+query])

	pass_list = {}

	pass_list.setdefault('tweet', [])

	res = es.search(size=5000, index="collectedtweets", doc_type="tweets", body={
		"query":{
			"match" : { "tweetmessage": query}
		}
	})
	# print("printing res")
	# print(res)

	for j in res['hits']['hits']:
		pass_list['tweet'].append(j['_source'])
		
	pass_list_final={}
	pass_list['query'] = query;
	pass_list_final = json.dumps(pass_list)

	return render(request,"index.html",{"my_data":pass_list_final})


