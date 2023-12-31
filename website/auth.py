from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from website import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user = models.User.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password_hash, user_password):
                flash("Logged in successfully!")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, please try again.")
                
        else:
            flash('Email does not exist.')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == 'POST':

        user_email = request.form['email']
        user_username = request.form['username']
        user_password = request.form['password']
        user_confirm_password = request.form['confirm_password']

        if len(user_email) < 5:
            flash('Email must be greater than 4 characters.')
        elif len(user_username) < 2:
            flash('Username must be greater than 1 characters.')
        elif user_password != user_confirm_password:
            flash('Passwords don\'t match.')
        else:
            new_user = models.User(email=user_email, username=user_username, password_hash=generate_password_hash(user_password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            return redirect(url_for('auth.login'))
    
    return render_template('signup.html', user=current_user)