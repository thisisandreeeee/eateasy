from flask import Flask, render_template, request
from yelp_handler import YelpHandler
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from ibm_handler import IBMHandler
import watsonibmtoneanalyzer
import ast
from urllib.parse import quote

app = Flask(__name__)

yh = YelpHandler()
ih = IBMHandler()

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        dic = {}
        dic['email'] = request.form.get('inputEmail')
        dic['dietary_preference'] = request.form.getlist('dietary_preference')
        dic['budget'] = request.form.get('budget')
        loc = request.form.get('autocomplete')
        if loc == '':
            loc = '88 Colin P Kelly Jr St, San Francisco, CA 94107'
        dic['location'] = loc.split(",")[0].strip()

        businesses = yh.get_nearby_businesses(dic, loc)
        limit = 3 # change this line
        business = choose_business(dic, businesses, limit)
        #coords = [(lat,lon,name) , ]
        coords=[]
        if business:
            for each_business in business:
                print(each_business['address'])
                geolocator = Nominatim()
                s=each_business['address']
                add=(" ").join(s)
                if(len(add)>3):
                    add=add[-3:]

                print(add)
                location = geolocator.geocode(add)
                coords.append((None if location==None else location.latitude,None if location==None else location.longitude,each_business['name']))
        else:
            business = []
            business.append({'url': 'http://www.yelp.com/biz/saison-san-francisco-2?adjust_creative=Tf6TJoFMH2Dy8i84-3ngHw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=Tf6TJoFMH2Dy8i84-3ngHw', 'joy': 0.54597585714285712, 'categories': ['American (New)'], 'contact': '+1-415-828-7990', 'address': ['178 Townsend St', 'SoMa', 'San Francisco, CA 94107'], 'name': 'Saison', 'rating': 4.5})
            business.append({'url': 'http://www.yelp.com/biz/alexanders-steakhouse-san-francisco?adjust_creative=Tf6TJoFMH2Dy8i84-3ngHw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=Tf6TJoFMH2Dy8i84-3ngHw', 'joy': 0.69379279999999999, 'categories': ['Steakhouses'], 'contact': '+1-415-495-1111', 'address': ['448 Brannan St', 'SoMa', 'San Francisco, CA 94107'], 'name': "Alexander's Steakhouse", 'rating': 4.0})
            business.append({'url': 'http://www.yelp.com/biz/benu-san-francisco-4?adjust_creative=Tf6TJoFMH2Dy8i84-3ngHw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=Tf6TJoFMH2Dy8i84-3ngHw', 'joy': 0.70858600000000005, 'categories': ['American (New)', 'Asian Fusion'], 'contact': '+1-415-685-4860', 'address': ['22 Hawthorne St', 'Financial District', 'San Francisco, CA 94105'], 'name': 'Benu', 'rating': 4.5})
        return render_template('results.html', lst = business, coords = coords)
    return render_template('form.html')

def choose_business(dic, lst, limit = 3):
    count = 0
    BUDGET_MAP = {
        '1-10': 1,
        '10-20': 2,
        '20-50': 3,
        '50+': 4
    }
    all_items = []
    for item in lst:
        r = requests.get(item['url'])
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            dollar_count = len(soup.find("span", { "class" : "price-range" }).text)
        except:
            pass
        budget = BUDGET_MAP[dic['budget']]
        if budget <= dollar_count:
            all_items.append(item)
            count += 1
        if count == limit:
            break
    for biz in all_items:
        joy_score = ih.twitterInfo(biz['name'])
        biz['joy'] = joy_score
    return all_items if all_items else None

# AKSHAY: i have added a new route here that you can reference
@app.route("/maps")
@app.route("/maps/<address>")
def maps(address=None):
    # if you want to return a html file called maps.html, uncomment the following line. you can pass an object to the render_template, kind of like what I did for the /form route
    add=' '.join(ast.literal_eval(address))
    #url_esc_str=quote(add)
    add=add.replace(' ','+')
    return render_template("maps.html",address=add)

@app.route("/tweets")
@app.route("/tweets/<business>")
def tweets(business=None):
    # if you want to return a html file called maps.html, uncomment the following line. you can pass an object to the render_template, kind of like what I did for the /form route
    result= watsonibmtoneanalyzer.TwitterInfo(business)
    return render_template("tweets.html",result=result)

@app.route("/") #TODO: temporary, remove later
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
