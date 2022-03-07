from flask import Flask, render_template, redirect, url_for, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def index_page():
    if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password") 
       return "Your name is "+username + password
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