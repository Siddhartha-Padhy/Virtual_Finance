from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/bank')
def bank_page():
    return render_template('bank.html')

@app.route('/stock')
def stock_page():
    return render_template('stock.html')

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)