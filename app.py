from flask import Flask, render_template, jsonify
from form import *
from model.user import User
import json

app = Flask(__name__)
app.secret_key = 'shushumushu'


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
        return render_template("choice.html", form = register_form)
    return render_template("registration.html", form = register_form)

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