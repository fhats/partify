from wtforms import Form 
from wtforms import PasswordField
from wtforms import TextField
from wtforms import validators

class RegistrationForm(Form):
    name = TextField("Your Full Name", [validators.Required(), validators.Length(min=4, max=64)])
    username = TextField('Username', [validators.Length(min=4, max=36), validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=36), validators.Required()])
    password = PasswordField('Password', [validators.Required()])
