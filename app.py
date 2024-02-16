from flask import Flask
from web.routes import webapp

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(webapp)
    app.run(debug=True)