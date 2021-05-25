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
from model.question_tag import Question_tag
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

@app.route("/qt", methods=["GET"])
def list_question_tags():
    result = []
    for question_tag in Question_tag.all():
        result.append(question_tag.to_dict())
    return jsonify(result), 201

@login_required
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
        new_question = Question(data['question'], "", current_user.name, data['choice'])
        new_question.save()
        
        for value in data['tags']:
            if value is not None:
                print(value)
                new_tag = Tag(value)
                new_tag.save()
                new_question_tag = Question_tag(new_question.id, new_tag.id)
                new_question_tag.save()
        
        chat_id = str(uuid.uuid1())
        print("NEW CHAT ID IS {}".format(chat_id))
        print("You are {}".format(matched_user.name))
        print("I am {}".format(current_user.name))
        emit('question_match', {'question': data['question'], 'user_id': current_user.id,
            'matched_user_id': matched_user.id, 'chat_id': chat_id}, room=matched_user.room_id)
    else:
        flash('No matches available. Try again!')
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

@socketio.on('display_question')
def display_question(data):
    print("display")
    user = User.find_by_name(str(data['username']))
    question = Question.find_most_recent_by_user(user.match)
    emit('display', {'question': question.content})

@socketio.on('save_answer')
def save_answer(data):
    print("save_answer")
    user = User.find_by_name(str(data['username']))
    question = Question.find_most_recent_by_user(user.match)
    print(question.content)
    Question.update_answer_by_content(str(data['answer']), question.content)

@login_required
@app.route('/rate/<username>', methods=["POST"] )
def rate(username):
    rating_user = current_user
    rated_user = User.find_by_name(username)
    print("Rating user is " + rating_user.name)
    print("Rated user is " + rated_user.name)

    #update rating and save in db    
    updated_rating = (rated_user.rating + int(request.form["rating"]))/2
    rated_user.update_rating(updated_rating)
    User.update_match("", rating_user.name)
    User.update_chat_id("None", rating_user.name)
    print("Updated rating is " + str(updated_rating))
    return redirect(url_for('ask'))


@socketio.on('filter')
def filter(data):
    print(data)
    # for tag in data['tags']:
    #     #find the tag 
    #     print("YOOYOYO")
    #     print(tag)
    #     existing_tag = Tag.find_by_content(tag)
    #     question_tag = Question_tag.find_by_tag_id(existing_tag.id)
    #     if existing_tag != 0:
    #     #add question that contains the tag to the list
    #         questions = Question_tag.search_by_tags()
    #         for q in question:
    print(data['tags'])
    questions = Question_tag.search_by_tags(data['tags'])
    r = [q.to_dict() for q in questions]
    emit('filter_result', {'result': r})
        
def send_message(content, username, room):
    current_time = strftime('%b-%d %I:%M%p', localtime())
    send({'msg': content, 'username': username, 'time_stamp': current_time}, room = room)

@socketio.on('message')
def message(data):
    send_message(data['msg'], data['username'], data['room'])

if __name__ == "__main__":
    socketio.run(app, debug=True)
