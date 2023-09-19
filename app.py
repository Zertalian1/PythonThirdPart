from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/api')
def info():
    return render_template('api_info.html')


if __name__ == '__main__':
    app.run()
