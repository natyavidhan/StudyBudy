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
for keys in config:
    app.config[keys] = config[keys]
backends = [Google]
database = Database()

@app.route('/')
def index():
    if 'user' in session:
        user =database.getUser(session['user']['_id'])
        return render_template('user.html', user=user)
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/boards')
def boards():
    if 'user' in session:
        boards = database.getBoards(session['user']['_id'])
        return render_template('boards/boards.html', boards=boards)
    return redirect(url_for('index'))

@app.route('/boards/new', methods=['POST'])
def new_board():
    if 'user' in session:
        database.addBoard(request.form['name'], session['user']['_id'])
        return redirect(url_for('boards'))
    return redirect(url_for('index'))

@app.route('/boards/<id>')
def board(id):
    if 'user' in session:
        board = database.getBoard(id, session['user']['_id'])
        if board is not None:
            return render_template('boards/board.html', board=board)
        return redirect(url_for('boards'))
    return redirect(url_for('index'))

def handle_authorize(remote, token, user_info):
    if not database.userExists(user_info['email']):
        database.addUser(user_info['email'])
    session['user'] = database.getUserByEmail(user_info['email'])
    return redirect(url_for('index'))

bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='/')
    
if __name__ == '__main__':
    app.run(debug=True)
