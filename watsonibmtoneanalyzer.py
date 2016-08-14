import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
   username='bb82f433-efb9-48e1-9adf-a66044818d3e',
   password='V0BS4sJSYaJ6',
   version='2016-05-19')



def TwitterInfo(business=None):
    twitter_consumer_key = 'SUTrY8wgL1FedNxNJzbPzuHxY'
    twitter_consumer_secret = 'ojzPDUon1Byfg5S1z95D1KAlcLVLcjj9eoBEDclGhBDVaeBI3T'
    twitter_access_token = '3426732497-SUCVH4zQUzjYfk8EnSzW6iuQ4FaYJyTh7SQVO3d'
    twitter_access_secret = 'GTR1iMos6E1TlseM4fm9n1zuVLQ6QWiorPulL4zD7XnZb'

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret,
                              access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

    temp = (twitter_api.GetSearch(term= business, count = '5'))
    #print(temp)
    '''for status in temp:
        print(status.user.name,status.user.profile_image_url , status.text,type(status.text))
    '''
    tweets=str(temp)
    tone=(json.dumps(tone_analyzer.tone(text=tweets), indent=2))
    print(tone)
    result={}
    result['tweets']=temp
    result['tone']=tone
    return result

#TwitterInfo()