from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import pie, user


@app.route("/add", methods = ["POST"])
def add():
    if "user_id" not in session:
        return redirect("/logout")
    if not pie.Pie.is_valid(request.form):
        return redirect("/dashboard")
    data = {
        "name" : request.form["name"],
        "filling" : request.form["filling"],
        "crust" : request.form["crust"],
        "user_id" : session["user_id"]
    }
    pie.Pie.save(data)
    return redirect('/dashboard')

@app.route("/derby")
def derby():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : session["user_id"]
    }
    pie = user.User.get_all_pies(data)
    return render_template("pies.html", pie = pie)

@app.route("/show/<int:id>")
def show(id) :
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    user_data = {
        "id" : session["user_id"]
    }
    return render_template("show.html", pie = pie.Pie.get_pie(data), users = user.User.get_by_id(user_data))

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    return render_template("edit.html", pie = pie.Pie.get_pie(data))

@app.route("/update", methods = ["POST"])
def update() :
    if "user_id" not in session:
        return redirect("/logout")
    if not pie.Pie.is_valid(request.form):
        return redirect("/dashboard")
    data = {
        "name" : request.form["name"],
        "filling" : request.form["filling"],
        "crust" : request.form["crust"],
        "id" : request.form["id"]
    }
    pie.Pie.update_pie(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id) :
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    pie.Pie.delete(data)
    return redirect("/dashboard")