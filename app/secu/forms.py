from flask_security.forms import RegisterForm, Required, LoginForm, StringField


class ExtendedRegisterForm(RegisterForm):
	username = StringField('username', [Required()])




class ExtendedLoginForm(LoginForm):
	# This is basically a hack to make it easy to login with both email
	# username. This is then modified in the config file
	# https://stackoverflow.com/questions/30827696/flask-security-login-via-username-and-not-email
	email = StringField("Username or Email Address", [Required()])