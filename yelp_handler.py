from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import config
from pprint import pprint

class YelpHandler:
    def __init__(self):
        auth = Oauth1Authenticator(
           consumer_key=config.consumer_key,
           consumer_secret=config.consumer_secret,
           token=config.token,
           token_secret=config.token_secret
        )
        self.client = Client(auth)

    def get_nearby_businesses(self, dic, location):
        params = {
            'lang': 'en',
            'limit': '20',
            'category_filter': ','.join([cat for cat in dic['dietary_preference'] if dic['dietary_preference']])
        }
        businesses = self.client.search(location, **params).businesses
        if businesses is not None:
            res = []
            for business in businesses:
                b = {}
                b['name'] = business.name
                b['address'] = business.location.display_address
                b['url'] = business.url
                b['contact'] = business.display_phone
                b['rating'] = business.rating
                b['categories'] = [i.name for i in business.categories]
                res.append(b)
            return res
        return None
