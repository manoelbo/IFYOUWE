from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, PasswordField, HiddenField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo,\
    NumberRange
from wtforms import ValidationError
from ..models import Role, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    facebook_id = IntegerField('FACEBOOK_ID(DONT CHANGE THIS! NEVER!)', validators=[Required()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class NewProjectForm1(Form):
    who = StringField('Who are you challenging?', validators=[Length(0, 64), Required(message=None)])
    what = StringField('What is the challenge?', validators=[Length(0, 80), Required(message=None)])
    couse = StringField('Which charity organization?', validators=[Length(0, 64), Required(message=None)])
    background_color = HiddenField()
    emoji1 = StringField()
    emoji2 = StringField()
    emoji3 = StringField()
    emoji4 = StringField()
    emoji5 = StringField(validators=[Required(message='You need to pick 5 emojis!')])
    submit = SubmitField('Create the card')

class NewProjectForm2(Form):
    why = TextAreaField('Why this challenge??', validators=[Length(0, 600), Required(message=None)])
    organization_website = HiddenField(validators=[Required(message='organization website is missing')])
    challenged_twitter = HiddenField()
    submit_step_2 = SubmitField('Submit challenge')


class EditProjectAdminForm(Form):
    who = StringField('Who are you challenging?', validators=[Length(0, 64)])
    what = StringField('What is the challenge?', validators=[Length(0, 80)])
    couse = StringField('Which charity organization?', validators=[Length(0, 64)])
    organization_name = StringField('What organization we will support?', validators=[Length(0, 64)])
    organization_url = StringField('Organization website:', validators=[Length(0, 64)])
    category = IntegerField('1-Collecting, 2-Waiting, 3-Win, 4-Fail', validators=[Required(), NumberRange(min=1, max=4)])
    about = TextAreaField('About:')
    approved = BooleanField('Approved?')
    submit = SubmitField('Submit')

class PaymentCheckout(Form):
    value = IntegerField('Value', validators=[Required()])

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class AmountForm(Form):
    amount_hidden = IntegerField(validators=[Required(), NumberRange(min=1, max=1000000000)])
    submit_amount = SubmitField('Submit donation')

