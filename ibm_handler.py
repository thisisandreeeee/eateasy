import sys
import operator
import requests
import json
import twitter
import config
import numpy as np
from watson_developer_cloud import ToneAnalyzerV3


class IBMHandler:

    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            username=config.ibm_user,
            password=config.ibm_pass,
            version='2016-05-19')
        self.twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key, consumer_secret=config.twitter_consumer_secret,access_token_key=config.twitter_access_token, access_token_secret=config.twitter_access_secret)

    def twitterInfo(self, business):
        temp = (self.twitter_api.GetSearch(term=business, count='5'))
        tweets = str(temp)
        tone_content = self.tone_analyzer.tone(text=tweets)
        score = []
        for line in tone_content['sentences_tone']:
            for cat in line['tone_categories']:
                if cat['category_id'] == 'emotion_tone':
                    for tone in cat['tones']:
                        if tone['tone_id'] == 'joy':
                            score.append(tone['score'])
        return np.mean(score)
