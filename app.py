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
        user = User(username, password, "Hasn't chosen", 5, sid, "None", "")
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
    #check if user has already chosen a category
    if current_user.choice != 'Hasn\'t chosen':
        flash('You have already chosen a category')
        return redirect(url_for('home'))
    #check if a category has been selected (hence POST)
    if request.method == "POST":
        category = request.form["category"]
        current_user.update_choice(category)
        return redirect(url_for("ask"))
    #if not
    else:
        return render_template("choice.html")

@app.route("/ask", methods=["GET"])
@login_required
def ask():
    print(current_user.name)
    if current_user.choice == 'Hasn\'t chosen':
        return redirect(url_for('choice'))
    return render_template("ask.html", user = current_user, questions = Question.find_by_user(current_user.name))

@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html", user = current_user)


@socketio.on('join_chat')
def join_chat(data):
    user = User.find_by_name(data['username'])
    join_room(user.chat_id)
    emit("joined", {'chat_id': user.chat_id}, room=user.room_id)

@socketio.on('join')
def join(data):
    print("Someone joined a room!!!\n")
    print(data['room'])
    print(data['username'])
    join_room(data['room'])

@socketio.on('leave')
def leave(data):
    print("Someone left a room!!!\n")
    print(data['room'])
    print(data['username'])
    leave_room(data['room'])
    # User.update_match("", str(data['username']))

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
    matched_user = User.find_closest_rating(data['choice'], data['rating'])
    if matched_user.is_authenticated:
        print("He is online!")
        question = Question(data['question'], "", current_user.name, data['choice'])
        question.save()
        
        for value in data['tags']:
            print(value)
            new_tag = Tag(value, question.id)
            new_tag.save()
        
        chat_id = str(uuid.uuid1())
        print("NEW CHAT ID IS {}".format(chat_id))
        print("You are {}".format(matched_user.name))
        print("I am {}".format(current_user.name))
        emit('question_match', {'question': data['question'], 'user_id': current_user.id,
            'matched_user_id': matched_user.id, 'chat_id': chat_id}, room=matched_user.room_id)
    else:
        print("No luck today!")
    


def update_matched_users(chat_id, asking_name, answering_name):
    User.update_chat_id(chat_id, asking_name)
    User.update_match(answering_name, asking_name)
    User.update_chat_id(chat_id, answering_name)
    User.update_match(asking_name, answering_name)


@socketio.on('redirect_asker')
def on_redirect_asker(data):
    print("CURRENT USER ON REDIRECT_ASKER {}".format(current_user.id))
    print("DATA IS {}".format(data))

    asking_user = User.find(int(data['user_id']))
    answering_user = User.find(int(data['matched_user_id']))
    print("ASKING IS {}, ANSWERING IS {}".format(asking_user.name, answering_user.name))
    #put both users in same chat_room and update match
    update_matched_users(str(data['chat_id']), asking_user.name, answering_user.name)
    
    emit('redirect', {'question': data['question'], 'chat_id': data['chat_id']}, room = asking_user.room_id)

@socketio.on('rate')
def rate(data):
    print("Rate function")
    print(data['name'])
    rating_user = User.find_by_name(str(data['name'])) #str?
    rated_user = User.find_by_name(rating_user.match)
    print("Rating user is " + rating_user.name)
    print("Rated user is " + rated_user.name)

    #update rating and save in db    
    updated_rating = (rated_user.rating + int(data['rating']))/2
    rated_user.update_rating(updated_rating)
    User.update_match("", rating_user.name)
    User.update_chat_id("None", rating_user.name)
    print("Updated rating is " + str(updated_rating))
    return redirect(url_for('home'))
    

@socketio.on('sort')
def sort(data):
    questions = []
    for tag in data['tags']:
        #find the tag 
        print("YOOYOYO")
        print(tag)
        newTag = Tag.find_by_content(tag)
        if newTag != 0:
        #add question that contains the tag to the list
            questions.append(Question.find_by_tag(newTag.question_id))
    #emit to function that displays questions containing tag
    if not questions:
        print("NO")
    emit('sort', {'questions': questions})
        
def send_message(content, username, room):
    current_time = strftime('%b-%d %I:%M%p', localtime())
    send({'msg': content, 'username': username, 'time_stamp': current_time}, room = room)

@socketio.on('message')
def message(data):
    send_message(data['msg'], data['username'], data['room'])

if __name__ == "__main__":
    socketio.run(app, debug=True)
