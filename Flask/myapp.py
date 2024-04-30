from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message
import sqlite3
import os
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

db_locale = 'users.db'
connection = sqlite3.connect(db_locale)

app = Flask(__name__)
app.secret_key = "MyFirstPythonApp"

@app.route("/")
@app.route('/login.html', endpoint='func1')
def login_page():
    return  render_template("login.html")

@app.route('/login.html', endpoint='func2')
def login_redirect(): 
    return render_template('login.html')

@app.route('/registration.html')
def reg_redirect():
    return render_template('registration.html')
 




@app.route('/authenticate', methods = ['GET', 'POST'])
def authenticate_user():
    if request.method == 'POST':
        login_user = (
            request.form['email'].lower(),
            request.form['pswd']
        )

        user = auth_user(login_user)

        if user == None:
            flash("User not found. Please register to gain access.")
            return render_template('login.html')
        
        elif user[3] == request.form['email'].lower():
            return render_template('home.html')
        
        else:
            flash("User not found. Please register to gain access.")
            return render_template('login.html')      


@app.route('/add', methods = ['GET', 'POST'])
def add_user():     
    if request.method == 'POST':    
        user_details = (
            request.form['fName'],
            request.form['lName'],
            request.form['email'].lower(),
            request.form['pswd1']
            )
        
    useremail = get_user(request.form['email'].lower())
    validuseremail = check_email(request.form['email'].lower())

    if request.form['pswd1'] == request.form['pswd2']:
        if useremail != request.form['email'].lower():
            if validuseremail == 'Valid Email':
                register_user (user_details)
                flash("Registration successful. Please log in")
                return render_template('login.html')
            else:
                flash("Please enter a valid email address.")
                return render_template('registration.html')
        else:
            flash("Email already exists. Please log in")
            return render_template('registration.html')
    else:
        flash("Passwords do not match.")
        return render_template('registration.html')









#Method 1 Authenticate User with Useremail and Password
def auth_user(login_user):
    connection = sqlite3.connect(db_locale)
    cursor = connection.cursor()
    sqlString = 'SELECT * FROM users WHERE user_email = ?  AND  user_pswd = ?'   
    cursor.execute(sqlString, login_user)
    user = cursor.fetchone()
    return user   

#Method 2 Register New user with Firstname, Lastname, email and Password
def register_user(user_details):
    connection = sqlite3.connect(db_locale)    
    cursor = connection.cursor()
    sqlString = 'INSERT INTO users (user_fName, user_lName, user_email, user_pswd) VALUES (?, ?, ?, ?)'        
    cursor.execute(sqlString, user_details)
    connection.commit()
    connection.close()

#Method 3 Chceck user with email - if email already exists or not for registration
def get_user(email):
    connection = sqlite3.connect(db_locale)
    cursor = connection.cursor()   
    cursor.execute("SELECT * FROM users WHERE user_email = '" + email + "'")   
    useremailadd = cursor.fetchone()

    if str(useremailadd) != 'None':
        if len(useremailadd) > 0:
            return useremailadd[3]  
        else:
            return 'None' 
    else:
        return 'None'
    
#Method 4 Chceck user email Valid or not
def check_email(email): 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return "Valid Email" 
    else:
        return "Invalid Email"

if __name__ == "__main__":
    app.run()