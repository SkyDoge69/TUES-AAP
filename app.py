from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from form import *
from model.user import User
import json

app = Flask(__name__)
app.secret_key = 'shushumushu'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data

        print(register_form.username.data)
        user = User(username, password, "Hasn't chosen")
        user.save()
        return redirect(url_for('login'))
    return render_template("registration.html", form = register_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return redirect(url_for('choice'))
    return render_template("login.html", form = login_form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('home'))

@app.route("/choice", methods=["GET", "POST"])
def choice():
    return render_template("choice.html")

@app.route("/users", methods=["GET"])
def list_users():
    result = []
    for user in User.all():
        result.append(user.to_viewable())
    return jsonify(result), 201

if __name__ == "__main__":
    app.run(debug=True)