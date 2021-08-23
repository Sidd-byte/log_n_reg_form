from log_reg_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from log_reg_app.models.user import User

@app.route('/')
def user():
    return render_template("index.html")



@app.route('/user/account', methods = ['post'])
def user_acc():

    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash =bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
    }

    user_id = User.save(data)

    session['logged_user'] = user_id
    return redirect('/dashboard')


@app.route('/user/login', methods = ['post'])
def user_login():
    data = {
        'email' : request.form['email']
    }
    retrieved_user = User.get_by_email(data)

    if not retrieved_user:
        flash("Wrong email or wrong password", "login_error")
        return redirect('/')

    if not bcrypt.check_password_hash(retrieved_user.password,request.form['password']):
        flash("Wrong email or wrong password", "login_error")
        return redirect('/')

    session['logged_user'] = retrieved_user.id

    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    data = {
        'id' : session['logged_user']
    }
    logged_user = User.get_one(data)
    return render_template('dashboard.html', user = logged_user)