from flask import Flask
from .0-hello_route import hello_hbnb

app = Flask(__name__)

app.register_blueprint(hello_hbnb)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
