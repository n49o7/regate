""" Web access. """

from flask import Flask, Response, render_template
# *, request, redirect
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route('/')
# @login_required
def main():
    return render_template('index.html')

@app.route('/data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    return Response(generate_random_data(), mimetype='text/event-stream')

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
