from flask import Flask, redirect, render_template, request, session, make_response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_migrate import Migrate
from time import time
import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# some required models


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(128))
    state = db.Column(db.String(64))
    city = db.Column(db.String(128))
    address = db.Column(db.String(1024))
    name = db.Column(db.String(128))
    phone = db.Column(db.String(20))
    beds = db.Column(db.Boolean)
    icu = db.Column(db.Boolean)
    oxygen = db.Column(db.Boolean)
    ventilator = db.Column(db.Boolean)
    tests = db.Column(db.Boolean)
    fabiflu = db.Column(db.Boolean)
    remdesivir = db.Column(db.Boolean)
    favipiravir = db.Column(db.Boolean)
    tocilizumab = db.Column(db.Boolean)
    plasma = db.Column(db.Boolean)
    food = db.Column(db.Boolean)
    generic = db.Column(db.Boolean)
    others = db.Column(db.Text)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-results',methods=["POST"])
def get-results():
    data = request.form


@app.route('/give-help', methods=["GET", "POST"])
def give_help():
    resources_raw = Resources.query.all()
    resources_raw.reverse()
    resources = resources_raw
    if request.method == "GET":
        return render_template('give-help.html',resources=resources)
    elif request.method == "POST":
        data = request.form
        # handle some exceptions and verify data here
        if data.get('state') == "none":
            return render_template('give-help.html', error="Please Choose Your State",resources=resources)
        # we are initializing variables here
        beds = False
        icu = False
        oxygen = False
        ventilator = False
        tests = False
        fabiflu = False
        remdesivir = False
        favipiravir = False
        tocilizumab = False
        plasma = False
        food = False
        generic = False
        resources = data.getlist('resources')
        if "beds" in resources:
            beds = True
        if "icu" in resources:
            icu = True
        if "oxygen" in resources:
            oxygen = True
        if "ventilator" in resources:
            ventilator = True
        if "tests" in resources:
            tests = True
        if "fabiflu" in resources:
            fabiflu = True
        if "remdesivir" in resources:
            remdesivir = True
        if "favipiravir" in resources:
            favipiravir = True
        if "tocilizumab" in resources:
            tocilizumab = True
        if "plasma" in resources:
            plasma = True
        if "food" in resources:
            food = True
        if "generic" in resources:
            generic = True
        state = data.get('state')
        city = data.get('city')
        name = data.get('name')
        phone = data.get('phone')
        address = data.get('address')
        others = data.get('others')
        resource = Resources(
            time= datetime.datetime.fromtimestamp(time()).strftime('%c'),
            state=state,
            city=city,
            address=address,
            name=name,
            phone=phone,
            beds=beds,
            icu=icu,
            oxygen=oxygen,
            ventilator=ventilator,
            tests=tests,
            fabiflu=fabiflu,
            remdesivir=remdesivir,
            favipiravir=favipiravir,
            tocilizumab=tocilizumab,
            plasma=plasma,
            food=food,
            generic=generic,
            others=others
        )
        db.session.add(resource)
        db.session.commit()
        resources_raw = Resources.query.all()
        resources_raw.reverse()
        resources = resources_raw
        return render_template('thanks.html',resources=resources)


if __name__ == '__main__':
    app.run(debug=True)
