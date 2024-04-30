from flask import Flask, render_template, request, flash, redirect
import sqlite3
import os

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

@app.route('/registration_success.html', endpoint='func3')
def registration_redirect(): 
    return render_template('login.html')

@app.route('/registration.html')
def reg_redirect():
    return render_template('registration.html')


@app.route('/authenticate', methods = ['GET', 'POST'])
def authenticate_user():
    if request.method == 'POST':
        login_user = (
            request.form['email'],
            request.form['pswd']
        )

        user = auth_user(login_user)

        if user == None:
            flash("User not found. Please register to gain access.")
            return render_template('login.html')
        
        elif user[3] == request.form['email']:
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
            request.form['email'],
            request.form['pswd1']
            )
        
    useremail = get_user(request.form['email'])

    if request.form['pswd1'] == request.form['pswd2']:
        if useremail != request.form['email']:
            register_user (user_details)
            flash("Registration successful. Please log in")
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
    user = cursor.fetchone()
    return user[3]  
    
if __name__ == "__main__":
    app.run()