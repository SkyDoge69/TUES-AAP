from flask import Flask, render_template, jsonify, redirect, url_for, flash, json, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, send, emit

from form import *
from model.user import User
import json
import uuid

app = Flask(__name__)
app.secret_key = 'shushumushu'
socketio = SocketIO(app)

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
        sid = str(uuid.uuid1())
        user = User(username, password, "Hasn't chosen", 5, sid)
        user.save()
        return redirect(url_for('choice'))
    return render_template("registration.html", form = register_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.find_by_name(login_form.username.data)
        login_user(user_object)
        return render_template("ask.html", username = current_user.name, rating = current_user.rating)
    return render_template("login.html", form = login_form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('home'))

@app.route("/choice", methods=["GET", "POST"])
def choice():
    return render_template("choice.html")

@app.route("/ask", methods=["GET", "POST"])
def ask():
    data = request.form['data']
    user = User.get_last_registered()
    user.update_choice(data, user.password)
    return redirect(url_for('login'))

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    return render_template("chat.html", username=current_user.name)

@app.route("/users", methods=["GET"])
def list_users():
    result = []
    for user in User.all():
        result.append(user.to_dict())
    return jsonify(result), 201

@socketio.on('message')
def message(data):
    print(f"\n\n{ data }\n\n")
    send(data)

@socketio.on('match')
def match(data):
    print("we are here")
    #check if user is online
    chosenOne = User.find_closest_rating(data['choice'], data['rating']) #info user
    print("Name: {}".format(chosenOne.name))
    print("Choice: {}".format(chosenOne.choice))
    print("Rating: {}".format(chosenOne.rating))
    print("Name: {}".format(chosenOne.id))
    emit('test', {'data': 33} )
    send("yo")
    return {"result" : "penis" }

if __name__ == "__main__":
    socketio.run(app, debug=True)