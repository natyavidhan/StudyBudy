from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import Database
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint, Google
from dotenv import dotenv_values
from datetime import datetime

app = Flask(__name__)
oauth = OAuth(app)
config = dotenv_values(".env")
config = dict(config)
app.secret_key = config["secret_key"]
for keys in config.keys():
    app.config[keys] = config[keys]
backends = [Google]
database = Database()

@app.route('/')
def index():
    if 'user' in session:
        return render_template('user.html', user=session['user'])
    return render_template('index.html')

def handle_authorize(remote, token, user_info):
    if database.userExists(user_info['email']):
        session['user'] = database.getUserByEmail(user_info['email'])
    else:
        database.addUser(user_info['email'])
        session['user'] = database.getUserByEmail(user_info['email'])
    return redirect(url_for('index'))

bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='/')
    
if __name__ == '__main__':
    app.run(debug=True)
