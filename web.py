""" Web access. """

from flask import Flask, render_template
# , request, redirect
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route('/')
# @login_required
def main():
    return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if request.method == 'POST':
#         data = request.form
#         return dashboard(data)
#     return render_template('login.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return dashboard(form)
#     return render_template('login.html', form=form)

# class LoginForm(FlaskForm):
#     class Meta:
#         csrf = False
#     URL = StringField('URL')
#     username = StringField('Username')
#     password = PasswordField('Password')
#     remember_me = BooleanField('Remember')
#     submit = SubmitField('Sign In')

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=23914)
