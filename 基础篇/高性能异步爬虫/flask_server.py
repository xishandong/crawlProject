from flask import Flask
import time

app = Flask(__name__)


@app.route('/dxs')
def index_dxs():
    time.sleep(2)
    return 'Hello dxs!'


@app.route('/dxy')
def index_dxy():
    time.sleep(2)
    return 'Hello dxy!'


@app.route('/date')
def index_date():
    time.sleep(2)
    return 'dxs date dxy!'


if __name__ == '__main__':
    app.run(threaded=True)
