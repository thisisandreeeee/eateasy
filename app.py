from flask import Flask, render_template, request
from yelp_handler import YelpHandler
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import watsonibmtoneanalyzer
import ast
from urllib.parse import quote

app = Flask(__name__)

yh = YelpHandler()

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
        print(coords)
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
            return all_items
    print(all_items)
    return all_items if all_items else None

# AKSHAY: i have added a new route here that you can reference
@app.route("/maps")
@app.route("/maps/<address>")
def maps(address=None):
    # if you want to return a html file called maps.html, uncomment the following line. you can pass an object to the render_template, kind of like what I did for the /form route
    '''
    geolocator = Nominatim()
    print(address,type(address))
    s=address.split(', ')
    add=(" ").join(s)
    print(s)
    location = geolocator.geocode(s)
    str=""
    for i in address:
        str=str+i
    print(address, type(address))
    '''
    add=' '.join(ast.literal_eval(address))
    #url_esc_str=quote(add)
    add=add.replace(' ','+')
    return render_template("maps.html",address=add)
    
@app.route("/tweets")
@app.route("/tweets/<business>")
def tweets(business=None):
    # if you want to return a html file called maps.html, uncomment the following line. you can pass an object to the render_template, kind of like what I did for the /form route
    result= watsonibmtoneanalyzer.TwitterInfo(business)
    print(result)
    return render_template("tweets.html",result=result)

@app.route("/") #TODO: temporary, remove later
def main():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug = True)
