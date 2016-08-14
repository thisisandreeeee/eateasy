from flask import Flask, render_template, request
from yelp_handler import YelpHandler
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
        business = choose_business(businesses)
        return render_template('results.html', business = business)
    return render_template('form.html')

def choose_business(lst):

    return lst[0]

@app.route("/") #TODO: temporary, remove later
def main():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug = True)
