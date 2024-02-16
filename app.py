from flask import Flask
from web.routes import webapp
from utils.folder_creation import check_init_folders

app = Flask(__name__)

if __name__ == '__main__':
    # Initial checks
    check_init_folders()

    # Start the web application
    app.register_blueprint(webapp)
    app.run(debug=True)