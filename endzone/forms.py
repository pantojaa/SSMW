from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from endzone.models import User
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    # DataRequired makes sure field is not empty
    # length puts restriction on length
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    # Email makes sure email address is valid
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Equals to compares the variable with specified one
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
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
    image = FileField('Attach files', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])


class UpdateProfile(FlaskForm):
    select_file = FileField('Attach files', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Post')
    update_profile = SubmitField('Update Profile')

