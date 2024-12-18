from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import logging
import numpy as np
import pandas as pd
import re

####*-------------------------------------------------------*###
#*                   Flask Configurations                     *#
####*-------------------------------------------------------*###
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'simple_login_database'

mysql = MySQL(app)

####*--------------------------------------------------------------------------------------------------------------------*###
#*======================================================Display Pages======================================================*#
####*--------------------------------------------------------------------------------------------------------------------*###
####--------------------------------------------------------###
#                             Login                           #
####--------------------------------------------------------###
#**#               Everyone             #**#
# Login Page (Default page)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # When the user presses log in button will trigger POST 
    if request.method == 'POST'  and 'name' in request.form and 'password' in request.form:
        name = request.form.get('name')
        password = request.form.get('password')
        position = request.form.get('position')

        try: # Get information from sql data (user table)
            with mysql.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Users where name = %s AND password= %s ", (name, password))
                    account = cursor.fetchone()

        except Exception as e:
            logging.error(f"Database error: {e}")
        
        # Check if name, id and function team is correct
        # If details are wrong (account will be empty and login will be unsuccessful)

        print("ACCOUNT")
        print(type(account))

        if account:
            session['name'] = account[0]
            session['password'] = account[3]
            session['position'] = account[4]

            # This part determines what type of user 
            # Type 1 is user
            # Type 2 is admin or manager
            position = session['position'].upper()
            if position == 'EMPLOYEE' or position == 'USER':
                session['user_type'] = 'user_type1'

            if position == 'ADMIN' or position == 'MANAGER':
                session['user_type'] = 'user_type2'


            # Check the user type
            user_type = session['user_type']

            # Flash a success message of login successful
            # Redirect user to display corresponding to type of user
            flash('Login Successful !', category='success')
            if  user_type == 'user_type1':
                return redirect(url_for('display1')) # user page
            elif  user_type == 'user_type2':
                return redirect(url_for('display2')) # Admin page
            else:
                return redirect(url_for('login')) # Failed login

        else:
            # flash an error message
            flash('Login unsuccessful !', category='error')

    return render_template('login.html')  


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'position' in request.form :
        name = request.form['name']
        password = request.form['password']
        age = request.form['age']
        position = request.form['position']    

        try: # Check if name is already regisered 
            with mysql.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Users where name = %s", (name,))
                    account = cursor.fetchone()

        except Exception as e:
            logging.error(f"Database error: {e}")

        if account:
            flash('Account already exists !', category='error')

        elif not re.match(r'[A-Za-z0-9]+', name):
            flash('Name must contain only characters and numbers !', category='error')

        elif not name or not password or not age or not position:
            flash('Please fill out the form !', category='error')
        else:
            try: # Check if name is already regisered 
                with mysql.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO Users (name, age, password, position) VALUES (%s, %s, %s, %s)", (name, age, password, position))
                    mysql.connection.commit()

                flash('You have successfully registered !', category='success')

                return render_template('display2.html')

            except Exception as e:
                logging.error(f"Database error: {e}")


    return render_template('register.html')




#**#               User               #**#
@app.route('/display1', methods=['GET', 'POST'])
def display1():
    name=session['name']
    password=session['password']

    if request.method == 'GET':
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users where name = %s AND password= %s ", (name, password))
                account = cursor.fetchone()

        except Exception as e:
            logging.error(f"Database error: {e}")

        # Convert the tuple to a dictionary using index positions as keys
        account_dict = {f'key{i}': value for i, value in enumerate(account)}

        
        return render_template('display1.html', account_dict=account_dict)
    

#**#           Admin/Manager            #**#
@app.route('/display2', methods=['GET', 'POST'])
def display2():
    name=session['name']
    password=session['password']

    if request.method == 'GET':
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users where name = %s AND password= %s ", (name, password))
                account = cursor.fetchone()

        except Exception as e:
            logging.error(f"Database error: {e}")

        # Convert the tuple to a dictionary using index positions as keys
        account_dict = {f'key{i}': value for i, value in enumerate(account)}

        
        return render_template('display1.html', account_dict=account_dict)

        
####---------------------------------------------------------###
#                            Logout                            #
####---------------------------------------------------------###   
@app.route('/logout')
def logout():
    # Clear everything
    session.clear()
    return redirect('/login')

####---------------------------------------------------------###
#                        Main Function                         #
####---------------------------------------------------------###
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)




