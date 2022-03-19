from flask import Flask, flash, render_template, redirect, url_for, request
from constants import *
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = str(getSecretKey())

@app.route('/', methods =["GET", "POST"])
def index_page():
    error = None
    if request.method == "POST":
        userEmail = str(request.form.get("userEmail"))
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        if request.form['sign'] == 'sign-in':
            try:
                username = validate_sign_in(userEmail,password)
                return redirect(url_for('home_page',user=username))
            except Exception as e:
                print('Error: ',e)
                error = 'Invalid Credentials'
    
        elif request.form['sign'] == 'sign-up':
            try:
                validate_sign_up(userEmail,username,password)
                return redirect(url_for('home_page',user=username))
            except Exception:
                error = 'Something went wrong!'

    return render_template('index.html',error=error)

@app.route('/home/<user>')
def home_page(user):
    available_stocks = get_my_stocks(user)
    worth = get_worth(user)
    return render_template('home.html', username=user, available_stocks=available_stocks, worth=worth)

@app.route('/stock/<user>', methods =["GET", "POST"])
def stock_page(user):
    stocks_today = get_stocks_api(URL)
    worth = get_worth(user)
    error = 'False'
    flash_message = ""

    if request.method == "POST":
        for index in range(7):
            data = request.form.items()
            for item,val in data:
                quantity = int(request.form.get(f'quantity{index+1}'))
                price = stocks_today[index]['inr']
                try:
                    if item == 'trade' and val == f'buy{index+1}':
                        stock_trade(user,index,price,quantity,True)
                    elif item == 'trade' and val == f'sell{index+1}':
                        stock_trade(user,index,price,quantity,False)
                except Exception as e:
                    error = 'True'
                    flash_message = str(e)
        worth = get_worth(user)

    available_stocks = get_my_stocks(user)

    return render_template('stock.html',stocks_today=stocks_today,username=user,available_stocks=available_stocks, worth=worth, error = error, flash_message=flash_message)

@app.route('/about/<user>')
def about_page(user):
    worth = get_worth(user)
    return render_template('about.html',username=user, worth=worth)

if __name__ == '__main__':
    app.run(debug=True)