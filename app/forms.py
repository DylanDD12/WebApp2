from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import HiddenField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

# Generate form fields


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='')])
    password = StringField('password', validators=[DataRequired(message='')])
    checkpass = StringField('checkpass', validators=[DataRequired(message='')])
    submit = SubmitField('Sign Up', name='signup_submit')


class LogInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='')])
    password = StringField('password', validators=[DataRequired(message='')])
    submit = SubmitField('Log In', name='login_submit')


class SetUpForm(FlaskForm):
    firstName = StringField('first', validators=[DataRequired(message='')])
    secondName = StringField('second', validators=[DataRequired(message='')])
    weight = IntegerField('weight', validators=[DataRequired(message='')])
    height = IntegerField('height', validators=[DataRequired(message='')])
    squat = IntegerField('squat', validators=[DataRequired(message='')])
    bench = IntegerField('bench', validators=[DataRequired(message='')])
    deadlift = IntegerField('deadLift', validators=[DataRequired(message='')])

    submit = SubmitField('Set Up', name='setup_submit')


class UpdateForm(FlaskForm):
    firstName = StringField('first')
    secondName = StringField('second')
    weight = IntegerField('weight')
    height = IntegerField('height')
    squat = IntegerField('squat')
    bench = IntegerField('bench')
    deadlift = IntegerField('deadLift')

    submit = SubmitField('Update', name='update_submit')


class GroupForm(FlaskForm):
    groupName = StringField('groupName', validators=[DataRequired(message='')])
    groupBio = StringField('groupBio', validators=[DataRequired(message='')])

    submit = SubmitField('Create Group', name='group_submit')


class JoinGroupForm(FlaskForm):
    groupName = HiddenField('groupName')


class LeaveGroupForm(FlaskForm):
    groupName = HiddenField('groupName')
