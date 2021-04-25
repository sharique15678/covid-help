from flask import Flask, redirect, render_template, request, session, make_response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_migrate import Migrate
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#some required models

class 

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()