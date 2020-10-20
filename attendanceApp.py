import pymongo
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime


class admin(object):

    @staticmethod
    def add_new_entry(sub, noa, a):
        data = {
            "day" : datetime.now().strftime("%d"),
            "month" : datetime.now().strftime("%m"),
            "year" : datetime.now().strftime("%y") + '20',
            "sub" : sub,
            "no_absentees" : noa,
            "absentees" : a
        }
        Database.insertion(data=data)

    @staticmethod
    def view():
        pass

    @staticmethod
    def find():
        pass


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['attendance']

    @staticmethod
    def insertion(data):
        Database.DATABASE['save'].insert_one(data)

    @staticmethod
    def find(query):
        return Database.DATABASE['save'].find(query)

    @staticmethod
    def find_one(query):
        return Database.DATABASE['save'].find_one(query)


app = Flask(__name__)
app.secret_key = "attendance_8f"


@app.route('/')
@app.route('/login')
def login_system():
    session['username'] = None
    return render_template('login.html')

@app.route('/home', methods=['POST', 'GET'])
def home_page():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "student_monitor":
        session['username'] = username
        return render_template("home.html", username=session['username'])
    else:
        session['username'] = None
        return render_template("wrong_login.html")

@app.route('/new_entry')
def new_entry():
    if session['username'] is not None:
        return render_template("new_entry.html")
    else:
        return render_template("wrong_login.html")

@app.route('/submit', methods=['POST','GET'])
def submit():
    if session['username'] is not None:
        Sub = request.form['subject']
        NoAbsents = request.form['NoOfAbsentees']
        NameAbsents = request.form['nameofabsentees']

        admin.add_new_entry(Sub, NoAbsents, NameAbsents)
        return render_template('submit.html')
    else:
        return render_template("wrong_login.html")

@app.route('/past_attendance')
def past_attendance_find():
    if session['username'] is not None:
        return render_template("Past_attendance.html")
    else:
        return render_template("wrong_login.html")

@app.route('/find_result', methods=['GET', 'POST'])
def find_result():
    if session['username'] is not None:
        a = dict()
        day_data = request.form['day']
        month_data = request.form['month']
        year_data = request.form['year']
        sub_data = request.form['subject']
        if day_data == "":
            pass
        else:
            a["day"] = day_data
        if month_data == "":
            pass
        else:
            a["month"] = month_data
        if year_data == "":
            pass
        else:
            a["year"] = year_data
        if sub_data == "":
            pass
        else:
            a["sub"] = sub_data
        b = Database.find_one(query = a)
        return render_template('find.html', results = b)
    else:
        return render_template("wrong_login.html")

@app.route('/logout')
def logout():
    session['username'] = None
    return render_template("Logout.html")


if True:
    Database.initialize()
    app.run(port=5000 ,debug=True)
