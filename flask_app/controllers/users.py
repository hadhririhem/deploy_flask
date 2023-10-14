from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import pie, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["POST"])
def register():
    if not user.User.is_valid(request.form) : 
        return redirect("/")
    password = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : password 
    }
    id = user.User.save(data)
    session["user_id"] = id 
    return redirect("/dashboard")

@app.route("/login", methods = ["POST"])
def login():
    users = user.User.get_by_email(request.form)
    if not users : 
        flash("invalid email")
        return redirect("/")
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("password incorrect")
        return redirect("/")
    session["user_id"] = users.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session : 
        return redirect("/logout")
    data = {
        "id" : session["user_id"]
    }
    users = user.User.get_by_id(data)
    pies = user.User.get_all_pies(data)
    return render_template("dashboard.html", users = users, pies = pies )

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')




