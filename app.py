import atexit
from flask import Flask, render_template
from keeper import MainKeeper

app = Flask(__name__)


keeper = MainKeeper()
keeper.run()
atexit.register(keeper.stop)


@app.route('/')
@app.route('/status')
def index():
    return render_template("status.html", title='Home', context=keeper.data)
