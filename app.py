from flask import Flask, render_template, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_migrate import Migrate
from time import time
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = "a secret key"
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
    resources = Resources.query.order_by(Resources.city).all()
    cities = []
    for resource in resources:
        cities.append(resource.city)  # creating list of cities in database
    cities = list(set(cities))  # removing duplicates
    cities.sort()  # sorting in alphabetical order
    return render_template('index.html', cities=cities)


@app.route('/get-results', methods=["POST"])
def get_results():
    data = request.form
    state = data.get('state')
    city = data.get('city')
    requirements = data.getlist('requirements')
    other = data.get('other')
    if state == 'none':
        resources = Resources.query.order_by(Resources.city).all()
        cities = []
        for resource in resources:
            cities.append(resource.city)  # creating list of cities in database
        cities = list(set(cities))  # removing duplicates
        cities.sort()  # sorting in alphabetical order
        return render_template('index.html', error="Please Choose Your State.",cities=cities)
    if len(requirements) == 0 and other == "" :
        resources = Resources.query.order_by(Resources.city).all()
        cities = []
        for resource in resources:
            cities.append(resource.city)  # creating list of cities in database
        cities = list(set(cities))  # removing duplicates
        cities.sort()  # sorting in alphabetical order
        return render_template('index.html', error="Please Choose something To Search.",cities=cities)
    # searching for some exact matches
    exact_results = query_db(requirements, city, state)
    # some approx matches
    approx_results = []
    raw_requirements = requirements
    print(len(requirements))
    for i in range(len(requirements)-2):
        print(i,"time")
        # index = (len(requirements)-1) - i
        raw_requirements.pop(raw_requirements.index(raw_requirements[-1]))
        approx_results = approx_results+query_db(raw_requirements,city,state)
        
    # now get single results for some single items
    single_results = query_single_db(requirements,city,state)

    # searching for other items not on list
    if other != "" :
        other_results_raw = Resources.query.filter(Resources.others.contains(other)).all()
    else :
        other_results_raw = []
    other_results_raw.reverse()
    other_results = other_results_raw

    results_raw = exact_results + other_results + approx_results + single_results
    results = []
    for result in results_raw :
        if result not in results :
            results.append(result)
        
    query = {
        "state" : state,
        "city" : city,
        "needs" : data.getlist('requirements'),
        "other" : other
    }
    return render_template('report.html',results=results,query=query)


def query_db(requirements, city, state): 
    # initialising variables
    beds = "beds" in requirements
    icu = "icu" in requirements
    oxygen = "oxygen" in requirements
    ventilator = "ventilator" in requirements
    tests = "tests" in requirements
    fabiflu = "fabiflu" in requirements
    remdesivir = "remdesivir" in requirements
    favipiravir = "favipiravir" in requirements
    tocilizumab = "tocilizumab" in requirements
    plasma = "plasma" in requirements
    food = "food" in requirements
    generic = "generic" in requirements
    # searching for matches
    resources = Resources.query.filter_by(
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
        state=state,
        city=city
    ).all()
    resources.reverse()
    results = resources
    return results

def query_single_db(requirements,city , state) :
    results = []
    for requirement in requirements :
        if "beds" == requirement:
            beds = Resources.query.filter_by(beds=True,city=city,state=state).all()
            beds.reverse()
            results = results + beds
        elif "icu" == requirement:
            icu = Resources.query.filter_by(icu=True,city=city,state=state).all()
            icu.reverse()
            results = results + icu
        elif "oxygen" == requirement:
            oxygen = Resources.query.filter_by(oxygen=True,city=city,state=state).all()
            oxygen.reverse()
            results = results + oxygen
        elif "ventilator" == requirement:
            ventilator = Resources.query.filter_by(ventilator=True,city=city,state=state).all()
            ventilator.reverse()
            results = results + ventilator
        elif "tests" == requirement:
            tests = Resources.query.filter_by(tests=True,city=city,state=state).all()
            tests.reverse()
            results = results + tests
        elif "fabiflu" == requirement:
            fabiflu = Resources.query.filter_by(fabiflu=True,city=city,state=state).all()
            fabiflu.reverse()
            results = results + fabiflu
        elif "remdesivir" == requirement:
            remdesivir = Resources.query.filter_by(remdesivir=True,city=city,state=state).all()
            remdesivir.reverse()
            results = results + remdesivir
        elif "favipiravir" == requirement:
            favipiravir = Resources.query.filter_by(favipiravir=True,city=city,state=state).all()
            favipiravir.reverse()
            results = results + favipiravir
        elif "tocilizumab" == requirement:
            tocilizumab = Resources.query.filter_by(tocilizumab=True,city=city,state=state).all()
            tocilizumab.reverse()
            results = results + tocilizumab
        elif "plasma" == requirement:
            plasma = Resources.query.filter_by(plasma=True,city=city,state=state).all()
            plasma.reverse()
            results = results + plasma
        elif "food" == requirement:
            food = Resources.query.filter_by(food=True,city=city,state=state).all()
            food.reverse()
            results = results + food
        elif "generic" == requirement:
            generic = Resources.query.filter_by(generic=True,city=city,state=state).all()
            generic.reverse()
            results = results + generic
    return results

@app.route('/give-help', methods=["GET", "POST"])
def give_help():
    resources_raw = Resources.query.all()
    resources_raw.reverse()
    resources = resources_raw
    if request.method == "GET":
        return render_template('give-help.html', resources=resources)
    elif request.method == "POST":
        data = request.form
        # handle some exceptions and verify data here
        if data.get('state') == "none":
            return render_template('give-help.html', error="Please Choose Your State", resources=resources)
        if len(data.getlist('resources')) == 0 and data.get('others') == "" :
            return render_template('give-help.html', error="Please Choose something.",resources=resources)
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
            time=datetime.datetime.fromtimestamp(time()).strftime('%c'),
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
        return render_template('thanks.html', resources=resources)


if __name__ == '__main__':
    app.run()
