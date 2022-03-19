import json
import requests
import pyrebase
from constants import *

def firebaseConfigRead():
    with open("C:/Users/Dell/OneDrive/Desktop/Python/fireConfig.json", 'r') as f:
        return json.load(f)

def getSecretKey():
    with open("C:/Users/Dell/OneDrive/Desktop/Projects/secret.txt", 'r') as f:
        return f.read()

firebaseConfig = firebaseConfigRead()
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

def validate_sign_in(userEmail,password):
    auth.sign_in_with_email_and_password(userEmail,password)
    data = db.child('Finance').child('Users').order_by_child('EmailId').equal_to(userEmail).get()
    for var in data.val():
        username = data.val()[var]['Username']
    return username

def validate_sign_up(userEmail,username,password):
    copies = db.child('Finance').child('Users').order_by_child('Username').equal_to(username).get()
    for copy in copies.each():
        if copy.val()!=None:
            raise Exception('Username already exists')
    worth = 50000
    data = {'Username':username,'EmailId':userEmail,'Worth':worth}
    auth.create_user_with_email_and_password(userEmail,password)
    db.child('Finance').child('Users').push(data)

def get_stocks_api(url):
    data=requests.get(url)
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

def get_worth(user):
    curr_user = db.child('Finance').child('Users').order_by_child('Username').equal_to(user).get()
    for var in curr_user.val():
        worth=curr_user.val()[var]['Worth']
    return worth

def get_my_stocks(user):
    stocks = db.child('Finance').child('Stocks').order_by_child('Owner').equal_to(user).get()
    data = []
    for stock in stocks.each():
        data.append(stock.val())
    return data

def update_worth(user,value,increase):
    curr_user = db.child('Finance').child('Users').order_by_child('Username').equal_to(user).get()
    if increase:
        curr_worth = int(get_worth(user))
        curr_worth = curr_worth + value

        for use in curr_user.each():
            if use.val()['Username'] == user:
                db.child('Finance').child('Users').child(use.key()).update({'Worth':curr_worth})

    else:
        curr_worth = int(get_worth(user))
        curr_worth = curr_worth - value

        for use in curr_user.each():
            if use.val()['Username'] == user:
                db.child('Finance').child('Users').child(use.key()).update({'Worth':curr_worth})

def stock_trade(user,index,price,quantity,buy):
    name = stocks_list[index].title()
    if buy:
        value = price * quantity
        if get_worth(user) < value:
            raise Exception('Not Enough Worth')
        avail_stocks = db.child('Finance').child('Stocks').order_by_child('Owner').equal_to(user).get()

        available = False
        for stock in avail_stocks.each():
            if stock.val()['Name'] == name:
                available = True
                curr = int(db.child('Finance').child('Stocks').child(stock.key()).child('Quantity').get().val()) + quantity
                db.child('Finance').child('Stocks').child(stock.key()).update({'Quantity':curr})

        if not available:
            data = {'Name':name,'Price':price,'Quantity':quantity,'Trade':'Buy','Owner':user}
            db.child('Finance').child('Stocks').push(data)

        update_worth(user,value,False)

    else:
        avail_stocks = db.child('Finance').child('Stocks').order_by_child('Owner').equal_to(user).get()
        for stock in avail_stocks.each():
            if stock.val()['Name'] == name:
                rem = int(db.child('Finance').child('Stocks').child(stock.key()).child('Quantity').get().val()) - quantity
                if rem > 0:
                    db.child('Finance').child('Stocks').child(stock.key()).update({'Quantity':rem})
                elif rem == 0:
                    db.child('Finance').child('Stocks').child(stock.key()).remove()
                else:
                    raise Exception('Not Enough Stocks')

        value = price * quantity
        update_worth(user,value,True)