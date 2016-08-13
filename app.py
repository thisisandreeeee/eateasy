from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        dic = {}
        dic['test'] = request.form.get('test')
        businesses = make_yelp_request(dic)
        business = choose_business(businesses)
        return render_template('results.html', business = business)
    return render_template('form.html')

def make_yelp_request(dic):
    return ['business1','business2']

def choose_business(lst):
    return lst[0]

@app.route("/") #TODO: temporary, remove later
def main():
    return render_template('results.html')
    
if __name__ == "__main__":
    app.run(debug = True)
