from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from model.user import User


def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data
    
    user_object = User.find_by_name(username_entered)
    if user_object is None:
        raise ValidationError("Wrong credentials!")
    elif password_entered != user_object.password:
        raise ValidationError("Wrong credentials!")

class RegistrationForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required"), 
    Length(min=4, max=25, 
    message="Username must be between 4 and 25 characters!")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), 
    Length(min=4, max=25, 
    message="Password must be between 4 and 25 characters!")])

    confirm_password = PasswordField('confirm_password_label',
    validators=[InputRequired(message="Password required"), 
    EqualTo('password', message = "Passwords must match")])

    submit_button = SubmitField('Register') 

    def validate_username(self, username):
        does_exist = User.find_by_name(username.data)
        if does_exist != None:
            raise ValidationError("Someone has taken this username, be more original!")

class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('login')
