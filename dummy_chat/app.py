from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
db = SQLAlchemy(app)

sessions = {}

class History(db.Model):
    id      = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    username = db.Column(db.String(256))
    msg = db.Column( db.String(500))
    

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def to_json(username, msg):
        return {
            'user' : username,
            'user_name' : msg.username,
            'message': msg.msg,
            'sent_date' : msg.date
        }

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/msg')
def session():
    return render_template('session.html')

@socketio.on('login_attempt')
def login(json, methods=['GET', 'POST']):
    global sessions
    if json['username'] not in sessions.values():
        tok = get_random_string(15)
        sessions[tok] = json['username']
        msg = {
            'user': json['username'],
            'tok': tok,
            'msg': '/msg'
        }
        socketio.emit('accept', msg)
    else:
        socketio.emit('decline', json)

@socketio.on('get_messages')
def send_hist(json, methods=['GET', 'POST']):
    tok = json['tok']
    global sessions
    if tok in sessions:
        for msg in History.query.all():
            socketio.emit('history', to_json(sessions[tok], msg) )
        newlogin = {
            'user_name': sessions[tok],
            'message': 'entered the chat',
            'sent_date': json['date']
        }
        socketio.emit('message', newlogin)
        message = message = History(username = newlogin['user_name'], date = json['date'],  msg = newlogin['message']) 
        db.session.add(message)
        db.session.commit()

@socketio.on('send_message')
def accept_message(json, methods=['GET', 'POST']):
    tok = json['tok']
    global sessions
    if tok in sessions and json['msg'] != '':
        socketio.emit('message', json['msg'])
        message = History(username = str(json['msg']['user_name']), date = json['msg']['sent_date'],  msg = str(json['msg']['message']) )
        db.session.add(message)
        db.session.commit()

@socketio.on('logout')
def logout(json, methods=['GET', 'POST']):
    global sessions
    torem = json['tok']
    newlogout = {
        'user_name': sessions[torem],
        'message': 'left chat',
        'sent_date': json['date']
    }
    message = message = History(username = newlogout['user_name'], date = json['date'],  msg = newlogout['message']) 
    db.session.add(message)
    db.session.commit()
    del sessions[torem]
    socketio.emit('message', newlogout)

if __name__ == '__main__':
    socketio.run( app, host='0.0.0.0')
