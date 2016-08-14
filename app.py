from flask import Flask, render_template, request
from yelp_handler import YelpHandler
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

yh = YelpHandler()

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        dic = {}
        dic['email'] = request.form.get('inputEmail')
        dic['dietary_preference'] = request.form.getlist('dietary_preference')
        dic['budget'] = request.form.get('budget')

        loc = '88 Colin P Kelly Jr St'
        businesses = yh.get_nearby_businesses(dic, loc)
        business = choose_business(dic, businesses)
        return render_template('results.html', business = business)
    return render_template('form.html')

def choose_business(dic, lst):
    BUDGET_MAP = {
        '1-10': 1,
        '10-20': 2,
        '20-50': 3,
        '50+': 4
    }
    for item in lst:
        r = requests.get(item['url'])
        soup = BeautifulSoup(r.text, 'html.parser')
        dollar_count = len(soup.find("span", { "class" : "price-range" }).text)
        budget = BUDGET_MAP[dic['budget']]
        if budget <= dollar_count:
            return item
    return None

@app.route("/") #TODO: temporary, remove later
def main():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug = True)
