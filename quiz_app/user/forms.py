from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from flask_login import current_user
from quiz_app import mongo

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = mongo.db.users.find_one({'username': username.data})
            if user:
                raise ValidationError('Username is already taken.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = mongo.db.users.find_one({'email': email.data})
            if user:
                raise ValidationError('Email is already registered.')