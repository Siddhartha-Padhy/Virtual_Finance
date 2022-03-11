from typing import OrderedDict
from flask import Flask, flash, render_template, redirect, url_for, request
import requests
import pyrebase
import json

def firebaseConfigRead():
    with open("C:/Users/Dell/OneDrive/Desktop/Python/fireConfig.json", 'r') as f:
        return json.load(f)

def getSecretKey():
    with open("C:/Users/Dell/OneDrive/Desktop/Projects/secret.txt", 'r') as f:
        return f.read()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(getSecretKey())

firebaseConfig = firebaseConfigRead()
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

stocks_list = ['bitcoin','cardano','dogecoin','ethereum','solana','tether','tron']
stocks = "%2C".join(stocks_list)
URL = f"https://api.coingecko.com/api/v3/simple/price?ids={stocks}&vs_currencies=INR&include_market_cap=true&include_24hr_vol=true&include_24hr_change=false&include_last_updated_at=false"

db = firebase.database()

def stock_trade(user,index,price,quantity,buy):
    if buy:
        print(f'Buy: {index}  {quantity}')
        data = {'Name':stocks_list[index],'Price':price,'Quantity':quantity,'Trade':'Buy'}
        db.child('Users').child(user).child('stock').push(data)

    else:
        print(f'Sell: {index}  {quantity}')
        data = {'Name':stocks_list[index],'Price':price,'Quantity':quantity,'Trade':'Sell'}
        db.child('Users').child(user).child('stock').push(data)

def get_stocks_api():
    data=requests.get(URL)
    result = data.json()
    stocks_today = []
    for key in result:
        ans = {}
        ans['Name'] = key.title()
        for k_val in result[key]:
            ans[k_val] = result[key][k_val]
        stocks_today.append(ans)
    stocks_today = sorted(stocks_today, key=lambda d: d['Name']) 
    return stocks_today

@app.route('/', methods =["GET", "POST"])
def index_page():
    error = None
    if request.method == "POST":
        userEmail = str(request.form.get("userEmail"))
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        if request.form['sign'] == 'sign-in':
            try:
                auth.sign_in_with_email_and_password(userEmail,password)
                flash('Successfully Signed in')
                return redirect(url_for('home_page',user=username))
            except Exception as e:
                print('Error: ',e)
                error = 'Invalid Credentials'
    
        elif request.form['sign'] == 'sign-up':
            try:
                data = {'EmailId':userEmail}
                auth.create_user_with_email_and_password(userEmail,password)
                db.child('Users').child(username).push(data)
                return redirect(url_for('home_page',user=username))
            except:
                error = 'Something went wrong!'

    return render_template('index.html',error=error)

@app.route('/home/<user>')
def home_page(user):
    return render_template('home.html',username=user)

@app.route('/bank/<user>')
def bank_page(user):
    return render_template('bank.html',username=user)

@app.route('/stock/<user>', methods =["GET", "POST"])
def stock_page(user):
    stocks_today = get_stocks_api()

    if request.method == "POST":
        for index in range(7):
            # if (request.form['trade'] == 'buy'+ str(index)) or (request.form['trade'] == 'sell'+ str(index)):
            data = request.form.items()
            for item,val in data:
                quantity = request.form.get(f'quantity{index}')
                price = stocks_today[index]['inr']
                if item == 'trade' and val == f'buy{index}':
                    stock_trade(user,index,price,quantity,True)
                elif item == 'trade' and val == f'sell{index}':
                    stock_trade(user,index,price,quantity,False)

    return render_template('stock.html',stocks_today=stocks_today,username=user)

@app.route('/contacts/<user>')
def contacts_page(user):
    return render_template('contacts.html',username=user)

if __name__ == '__main__':
    app.run(debug=True)