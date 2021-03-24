from flask import request, redirect, render_template, abort, flash, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.main import app, login_manager
from app.models.user import User 
from app.db import db


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).one_or_none():
            error = "This email is already registered."
            return render_template("register.html", name=username, email=email, password=password, error=error)

        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).one_or_none()
        error = None
        
        if not user:
            error = 'No user with email %s exists.' % email
        elif not check_password_hash(user.password, password):
            error = 'Password does not match email.'
        
        if error:
            return render_template("login.html", error=error, email=email, password=password)
        
        login_user(user)
        return redirect(url_for("dashboard"))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))        

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login"))
