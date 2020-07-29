from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from endzone.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class RegistrationForm(FlaskForm):
    first_name = StringField('First name*', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name*', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password*', validators=[DataRequired(), EqualTo('password')])
    gender = StringField('Gender*')
    birthday = StringField('Birthday*')
    city = StringField('City*')
    state = StringField('State*')
    high_school = StringField('Current school', validators=[])
    sport = StringField('Sport', validators=[])
    position = StringField('Position', validators=[])
    submit = SubmitField('Sign up')

    # Checks to see if email is already within database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already being used. Please select another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[])
    submit = SubmitField('Post')
    delete = SubmitField('Delete')
    edit = SubmitField('Edit')
    image = FileField('Attach files', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'mp4'])])


class UpdateProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('About me')
    high_school = StringField('Current school', validators=[])
    sport = StringField('Sport', validators=[])
    position = StringField('Position', validators=[])
    city = StringField('City')
    state = StringField('State')
    select_file = FileField('Update profile picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    banner = FileField('Update banner', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Save changes')
    update_profile = SubmitField('Update Profile')

    def validate_first_name(self, first_name):
        if first_name.data != current_user.first_name:
            user = User.query.filter_by(email=first_name.data).first()
            if user:
                raise ValidationError('Please enter a different first name.')

    def validate_last_name(self, last_name):
        if last_name.data != current_user.first_name:
            user = User.query.filter_by(email=last_name.data).first()
            if user:
                raise ValidationError('Please enter a different first name.')

    # Checks to see if email is already within database
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already being used. Please select another one.')


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')
