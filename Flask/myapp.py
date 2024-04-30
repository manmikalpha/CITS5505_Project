from flask import Flask, render_template, request
import sqlite3
import os

db_locale = 'users.db'
connection = sqlite3.connect(db_locale)

app = Flask(__name__)

@app.route("/")
@app.route('/login.html', endpoint='func1')
def login_page():
    return  render_template("login.html")

@app.route('/login.html', endpoint='func2')
def index(): 
    return render_template('login.html')

@app.route('/registration.html')
def index():
    return render_template('registration.html')

@app.route('/authenticate', methods = ['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        login_user = (
            request.form['email'],
            request.form['pswd']
        )

        auth_user(login_user)
        return None

@app.route('/add', methods = ['GET', 'POST'])
def add_user():     
    if request.method == 'POST':    
        user_details = (
            request.form['fName'],
            request.form['lName'],
            request.form['email'],
            request.form['pswd1']
            )
    
    register_user (user_details)
    return render_template('registration_success.html')


def auth_user(login_user):
    connection = sqlite3.connect(db_locale)

    cursor = connection.cursor()
    sqlString = 'SELECT * FROM users WHERE user_email = ?  AND  user_pswd = ?'
   
    cursor.execute(sqlString, login_user)
    user = cursor.fetchone()

    print (user)
   
    connection.commit()
    connection.close()
   

def register_user(user_details):
    connection = sqlite3.connect(db_locale)

    cursor = connection.cursor()
    sqlString = 'INSERT INTO users (user_fName, user_lName, user_email, user_pswd) VALUES (?, ?, ?, ?)'
   
    cursor.execute(sqlString, user_details)

    connection.commit()
    connection.close()



if __name__ == "__main__":
    app.run()