from flask import Flask, render_template

from satnogsclient import settings as client_settings


app = Flask(__name__)


@app.route('/')
def status():
    '''View status satnogs-client.'''
    return render_template('status.j2')

@app.route('/notify' ,  methods=['GET', 'POST'])
def notify():
    params = request.get_json()
    print params[0]
    


@app.route('/control/')
def control():
    '''Control satnogs-client.'''
    return render_template('control.j2')


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
