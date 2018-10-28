from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Email
# from flask_table import Table, Col
from flask_babel import _, lazy_gettext as _l
from app.models import User, Contact
from flask_login import current_user



class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

#todo add contact form
class ContactForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    phone_no = IntegerField(_l('Contact Number'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Submit'))

    #validating new contact
    def validate_email(self, email):
        email = Contact.query.filter_by(email=self.email.data,user_id=current_user.id).first()
        if email is not None:
            raise ValidationError(_('Contact already added!'))

# class ContactsView(Table):
#     id = Col('Id', show=False)
#     name = Col('Name')
#     phone_no = Col('Contact Number')
#     email = Col('Email Id')