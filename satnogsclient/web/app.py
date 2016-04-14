from flask import Flask, render_template, request, json, jsonify

from satnogsclient import settings as client_settings
from satnogsclient.scheduler import tasks
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer.commsocket import Commsocket


app = Flask(__name__)


@app.route('/')
def status():
    '''View status satnogs-client.'''
    sock1 = Commsocket('127.0.0.1',5005)
    
    #sock2 = Udpsocket('127.0.0.1',5006)
    b = sock1.connect()
    if b:   
        print sock1.send("Hello there\n")     
    else:
        print 'No observation currently'

    return render_template('status.j2')


@app.route('/control/')
def control():
    '''Control satnogs-client.'''
    sock = Commsocket('127.0.0.1',5011)
    b = sock.connect()
    if b:
        sock.send("Hello there\n")   
    else:
        print 'Task feeder thread not online'
    
    return render_template('control.j2')

@app.route('/notify' ,  methods=['GET', 'POST'])
def notify():
     params = request.get_json()
     print params['tle']
     return 'OK'
     
     
@app.route('/configuration/')
def configuration():
    '''View list of satnogs-client settings.'''
    filters = [
        lambda x: not x.startswith('_'),
        lambda x: x.isupper()
    ]

    entries = client_settings.__dict__.items()
    settings = filter(lambda (x, y): all(f(x) for f in filters), entries)

    ctx = {
        'settings': sorted(settings, key=lambda x: x[0])
    }

    return render_template('configuration.j2', **ctx)



    



