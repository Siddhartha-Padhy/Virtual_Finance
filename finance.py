from flask import Flask, render_template, redirect, url_for, request
import requests
import pyrebase
import json

def firebaseConfigRead():
    with open("C:/Users/Dell/OneDrive/Desktop/Python/fireConfig.json", 'r') as f:
        return json.load(f)

app = Flask(__name__)

firebaseConfig = firebaseConfigRead()
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

@app.route('/', methods =["GET", "POST"])
def index_page():
    if request.method == "POST":
        if request.form['sign'] == 'sign-in':
            username = request.form.get("username")
            password = request.form.get("password")
            try:
                auth.sign_in_with_email_and_password(username,password)
                return render_template('home.html',username=username)
            except:
                print("Failed")
        elif request.form['sign'] == 'sign-up':
            username = request.form.get("username")
            password = request.form.get("password")
            auth.create_user_with_email_and_password(username,password)
            return render_template('home.html',username=username)

    return render_template('index.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/bank')
def bank_page():
    return render_template('bank.html')

@app.route('/stock')
def stock_page():
    stocks_list = ['bitcoin','ethereum','tether','tron','solana','cardano','dogecoin']
    stocks = "%2C".join(stocks_list)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={stocks}&vs_currencies=INR&include_market_cap=true&include_24hr_vol=true&include_24hr_change=false&include_last_updated_at=false"

    data=requests.get(url)
    result = data.json()
    stocks_today = []
    for key in result:
        ans = {}
        ans['Name'] = key.title()
        for k_val in result[key]:
            ans[k_val] = result[key][k_val]
        stocks_today.append(ans)

    return render_template('stock.html',stocks_today=stocks_today)

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)