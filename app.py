from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
from form import *
from time import localtime, strftime

from errors import register_error_handlers
from login import login_manager
from model.user import User
from model.question import Question
from model.tag import Tag
import uuid

app = Flask(__name__)
app.secret_key = 'shushumushu'
socketio = SocketIO(app)
register_error_handlers(app)
login_manager.init_app(app)


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
        return redirect(url_for('ask'))
    return render_template("login.html", form = login_form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('home'))

@app.route("/choice", methods=["GET", "POST"])
@login_required
def choice():
    if current_user.choice != 'Hasn\'t chosen':
        flash('You have already chosen a category')
        return redirect(url_for('home'))
    if request.method == "POST":
        category = request.form["category"]
        # TODO: Validate category
        current_user.update_choice(category)
        return redirect(url_for("ask"))
    else:
        return render_template("choice.html")

@app.route("/ask", methods=["GET"])
@login_required
def ask():
    if current_user.choice == 'Hasn\'t chosen':
        return redirect(url_for('choice'))
    return render_template("ask.html", user = current_user)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html", username=current_user.name, room_id = current_user.room_id)

@socketio.on('join')
def join(data):
    print("EYOOOO\n")
    print(data['room'])
    print(data['username'])
    join_room(data['room'])
    User.update_room(str(data['room']), str(data['username']))

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])

@app.route("/users", methods=["GET"])
def list_users():
    result = []
    for user in User.all():
        result.append(user.to_dict())
    return jsonify(result), 201

@app.route("/questions", methods=["GET"])
def list_questions():
    result = []
    for question in Question.all():
        result.append(question.to_dict())
    return jsonify(result), 201

@app.route("/tags", methods=["GET"])
def list_tags():
    result = []
    for tag in Tag.all():
        result.append(tag.to_dict())
    return jsonify(result), 201

@app.route("/archive", methods=["GET"])
def archive():
    return render_template("archive.html", questions = Question.all_questions())

@socketio.on('message')
def message(data):
    print(f"\n\n{ data }\n\n")
    send(data)

@socketio.on('match')
def match(data):
    matchedUser = User.find_closest_rating(data['choice'], data['rating'])
    # TODO: Filter me!
    room_id = str(uuid.uuid4())
    question = Question(data['question'], "", current_user.name, data['choice'])
    question.save()
    for value in data['tags']:
        new_tag = Tag(value, question.id)
        new_tag.save()
    
    print("NEW ROOM ID IS {}".format(room_id))
    print("You are {}".format(matchedUser))
    print("I am {}".format(current_user))
    emit('question_match', {'question': data['question'], 'user_id': current_user.id,
                            'room_id': room_id}, room=matchedUser.room_id)

@socketio.on('redirect_asker')
def on_redirect_asker(data):
    print("CURRENT USER ON REDIRECT_ASKER {}".format(current_user.id))
    print("DATA IS {}".format(data))
    user = User.find(int(data['user_id']))
    emit('redirect', {'question': data['question'], 'room_id': data['room_id']}, room = user.room_id)

@socketio.on('rate')
def rate(data):
    print(str(data['room']))
    user = User.find_by_room_id(current_user.name, str(data['room']))
    new_rating = (user.rating + int(data['rating']))/2
    user.rating = new_rating
    user.save()
    print("znaeee6")
    # emit('question_match', {'question': data['question'], 'user_id': current_user.id,
    #                         'room_id': room_id}, room=chosenOne.room_id)


def send_message(content, username, room):
    current_time = strftime('%b-%d %I:%M%p', localtime())
    send({'msg': content, 'username': username, 'time_stamp': current_time}, room = room)

@socketio.on('message')
def message(data):
    send_message(data['msg'], data['username'], data['room'])

if __name__ == "__main__":
    socketio.run(app, debug=True)
