from flask import Flask, render_template, request, redirect, flash, session
#mysql import
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "secret_stuff"
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sucess',methods=["POST"])
def success():
    input_password=request.form['password']
    query = "SELECT * FROM users WHERE email = :email"
    data = {
        'email': request.form['email']
    }
    user= mysql.query_db(query,data)

    if user:
        for x in user:
            if bcrypt.check_password_hash(x['password'],input_password):
                return render_template("sucess.html")
            else:
                flash("Incorrect Password")
                return redirect("/")
    else:
        flash("Incorrect Email")
        return redirect("/")




@app.route('/register', methods=["POST"])
def register():
    query = "SELECT * FROM users WHERE email = :email"
    data = {
        'email': request.form['email']
    }
    results = mysql.query_db(query,data) # [] , [{}]

    if len(results) > 0:
        flash('Email already in use')
        return redirect('/')
    elif len(request.form['first_name'])<2:
        flash("First Name must be more than 2 charachters")
        return redirect('/')
    elif len(request.form['last_name'])<2:
        flash("Last Name must be more than 2 charachters")
        return redirect('/')
    else:
        if len(request.form['password']) < 8:
            flash('password not long enough')
            return redirect('/')
        elif request.form['password'] !=  request.form['password_confirmation']:
            flash("Passwords Dont Match")
            return redirect('/')
        else:
            enc_password = bcrypt.generate_password_hash(request.form['password'])
            query = "INSERT INTO users (email, password, first_name,last_name,created_at, updated_at) VALUES (:email, :password,:first_name,:last_name, NOW(), NOW())"
            data = {
                'email': request.form['email'],
                'password': enc_password,
                'first_name':request.form['first_name'],
                'last_name':request.form['last_name']


            }
            mysql.query_db(query,data)
            flash("Succesful Registration, Please login")
            return redirect('/')

app.run(debug=True)
