from flask import Flask, render_template

from satnogsclient.observer.commsocket import Commsocket
from satnogsclient import settings as client_settings


app = Flask(__name__)


@app.route("/")
def index():
    """View list of satnogs-client settings."""
    sock1 = Commsocket('127.0.0.1', 5005)
    b = sock1.connect()
    if b:
        sock1.send("Request")
    else:
        print 'No observation currently'

    filters = [
        lambda x: not x.startswith('_'),
        lambda x: x.isupper()
    ]

    entries = client_settings.__dict__.items()
    settings = filter(lambda (x, y): all(f(x) for f in filters), entries)

    ctx = {
        'settings': sorted(settings, key=lambda x: x[0])
    }

    return render_template('index.j2', **ctx)
