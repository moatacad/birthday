from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email,Length,EqualTo

class Signup(FlaskForm):
    username=StringField("username: ", validators=[DataRequired(),Length(min=6,max=8)])
    pwd=PasswordField("Password: ",validators=[DataRequired()])
    confirmpwd=PasswordField("Confirm Password: ",validators=[DataRequired(),EqualTo('pwd',message="The confirm password must be equal to the password field")])
    submit = SubmitField("Signup")

class Login(FlaskForm):
    username=StringField("username: ", validators=[DataRequired(),Length(min=6,max=8)])
    pwd=PasswordField("Password: ",validators=[DataRequired()])
    loginbtn = SubmitField("Login")

class ProfileForm(FlaskForm):
    email =StringField('Email', validators=[DataRequired(),Email()])
    guest_fullname = StringField("Fullname: ", validators=[DataRequired()])
    userstate = SelectField('State', choices=[('', 'select'),('1', 'Lagos')])
    updatebtn = SubmitField("Update Details")

class DonationForm(FlaskForm):
    gift1 = BooleanField('Clothes')
    gift2 = BooleanField('Cash')
    gift3 = BooleanField('Laptop')
    gift4 = BooleanField('Shoes')
    msg = TextAreaField('Message')
    btn = SubmitField('Donate')

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),FileAllowed(['jpg','png'],"Please ensure you are uploading ONLY Images")])
    btn = SubmitField('Upload Now!')

class ContactForm(FlaskForm):
    email =StringField('Email', validators=[DataRequired(),Email()])
    fullname = StringField("Fullname: ", validators=[DataRequired()])
    msg = TextAreaField('Message')
    sendbtn = SubmitField("Send Message")