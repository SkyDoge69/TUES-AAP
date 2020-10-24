from flask import Flask, render_template, jsonify
from form import *
from model.user import User
import json

app = Flask(__name__)
app.secret_key = 'shushumushu'


@app.route("/", methods=["GET", "POST"])
def index():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data

        # have to check if username already in use
        user = User(username, password)
        print(user.name)
        print(user.password)
        print(user.id)
        user.save()
        return render_template("choice.html", form = register_form)
    return render_template("index.html", form = register_form)

@app.route("/users", methods=["GET"])
def list_users():
    result = []
    for user in User.all():
        result.append(user.to_viewable())
    return jsonify(result), 201

if __name__ == "__main__":
    app.run(debug=True)