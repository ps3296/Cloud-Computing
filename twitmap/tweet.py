from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys
import elasticsearch
from elasticsearch import Elasticsearch




#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.



#consumer key, consumer secret, access token, access secret.


es = elasticsearch.Elasticsearch([{u'host':u'127.0.0.1', u'port': b'9200'}]) 

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        #print all_data
        #print ("\n")
        tweet = all_data["text"]        
        username = all_data["user"]["screen_name"]
        location = all_data["user"]["location"]
        if all_data['coordinates']:
                lon = float(json_data['coordinates']['coordinates'][0])
                print(lon)
        elif 'place' in all_data.keys() and all_data['place']:
            place = all_data['place']['bounding_box']['coordinates'][0][0][1]
            print(place)
         

        
        if 'text' in all_data:

            doc={
            #es.index(index='tweets', doc_type='tweets', body={
                'username':username,
                'tweet':tweet,
                'location': location,
                #'filter': sys.argv[1],
                }
        s = es.index(index='tweets', doc_type='tweets', body=doc)
    
        
        
        print((location))
        
        print ("\n")
        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
#twitterStream.filter(track=["#" + sys.argv[1]])
twitterStream.filter(track=["#trump"])

