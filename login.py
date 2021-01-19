from flask import redirect, url_for
from flask_login import LoginManager
from model.user import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
