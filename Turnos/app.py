
import sys
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import datetime
from functools import wraps
from itsdangerous import URLSafeTimedSerializer as Serializer


app = Flask(__name__)

CUBICLE = ["1","2","3","4","5","6","7","8","9","10"]

BANK = [
    "Withdrawals",
    "Advisory",
    "Inquiries",
    "Help",
    "Loans",
    "Payments"
]

HOSPITAL = [
    "Emergency",
    "Service Post Emergency",
    "Urgency",
    "Medical Appoiment",
    "Drugs",
    "General Help"
]

OPTIONS = [
    "Bank",
    "Hospital"
]

SIZE = [
    "Microentreprises (1 to 9 employees)",
    "Small enterprises (10 to 49 employees)",
    "Medium-sized enterprises (50 to 249 employees)",
    "Large enterprises (250 employees or more)"
]

### no supe implementar password reset con token para que eniara un codigo al correo electronico establecido por eso se utiliza las security questions###
QUESTION = [
    "What was the name of the boy or the girl you first kissed?",
    "Where were you when you had your first kiss?",
    "In what city did you meet your spouse/significant other?",
    "What is the middle name of your youngest child?",
    "What was the name of your first stuffed animal?", 
    "In what city or town did your mother and father meet?",
    "What was the first exam you failed?",
    "What was the name of your first school teacher?",
    "What year did you enter college?",
    "What is your grandmother’s maiden name?",
    "What is your child’s nickname?",
    "What is the manufacturer of your first car?",
    "What was your childhood best friend’s nickname?",
    "In which city did your parents meet?",
    "What’s your neighbor’s last name?",
    "How many pets did you have at 10 years old?",
    "What month did you get married?",
    "In which city did your mother born?"
]

GENDER = [
    "Male",
    "Female",
    "Other"
]

ID = [
    "Passport",
    "State ID",
    "Foreign ID",
    "Social Security",
    "Driver License"
]

TURNOS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
STAFFTURNOS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///turnos.db")

def apology():
    return render_template("apology.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



def company():
    id = session.get("user_id")
    user_id = id
    rowscompany = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    companytype = rowscompany[0]["business"]
    COMPANY = companytype
    return COMPANY
    
@app.route("/", methods=["GET", "POST"])
def login():
    session.clear()
    email = request.form.get("email")
    password = request.form.get("password")
    
    if request.method == "POST":
        if not email or not password:
            error = "No email or not password was found, please put your email or password!"
            return render_template("homepage.html")
        rows = db.execute("SELECT * FROM user WHERE email = ?", email)
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            error = "Invalid email or password! Try again!"
            return render_template("homepage.html", error=error)
        session["user_id"] = rows[0]["id"]
        print("logged in")
        return redirect("/home")
    return render_template("homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    confirmpassword = request.form.get("confirm_password")
    business = request.form.get("business")
    size = request.form.get("size")
    phone = request.form.get("phone")
    security = request.form.get("securityquestion")
    answer = request.form.get("answer")
    date = datetime.datetime.now()
    if request.method == "POST":
        if not email:
            error = "No email was found, please put your email"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not password:
            error = "No password was found, please put your password"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not confirmpassword:
            error = "No password confirmation was found, please put it"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if password != confirmpassword:
            error = "password its not the same as confirm password, please check it"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not business:
            error = "No business was selected, please select it"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not size:
            error = "No size was selected, please select it"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not phone:
            error = "No phone was found, please put your phone"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not security:
            error = "No security question was selected, please select it"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        if not answer:
            error = "No answer was found, please put your answer"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        rows = db.execute("SELECT * FROM user WHERE email = ?", email)
        if len(rows) != 0:
            error = "email is already used!"
            return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION, error=error)
        hash = generate_password_hash(password)
        db.execute("INSERT INTO user (email, hash, business, size, phone, security, answer, signupdate) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", email, hash, business, size, phone, security, answer, date)
        rows = db.execute("SELECT * FROM user WHERE email = ?", email)
        session["user_id"] = rows[0]["id"]
        print(session["user_id"])
        return redirect("/home")
    return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION)

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    email = request.form.get("email")
    phone = request.form.get("phone")
    security = request.form.get("securityquestion")
    answer = request.form.get("answer")
    password = request.form.get("newpassword")
    newpassword = request.form.get("confirmnewpassword")
    if request.method == "POST":
        if not email or not phone or not security or not answer or not password or not newpassword:
            error = "Missing information!"
            return render_template("forgot.html", question=QUESTION, error=error)
        if password != newpassword:
            error = "password and new password are not the same!"
            return render_template("forgot.html", question=QUESTION, error=error)
        rows = db.execute("SELECT * FROM user WHERE email = ?", email)
        if email != rows[0]["email"]:
            error = "information mismatch!"
            print("1")
            return render_template("forgot.html", question=QUESTION, error=error)
        if int(phone) != int(rows[0]["phone"]):
            print("2")
            error = "information mismatch!"
            return render_template("forgot.html", question=QUESTION, error=error)
        if security != rows[0]["security"]:
            print("3")
            error = "information mismatch!"
            return render_template("forgot.html", question=QUESTION, error=error)
        if answer != rows[0]["answer"]:
            print("4")
            error = "information mismatch!"
            return render_template("forgot.html", question=QUESTION, error=error)
        hash = generate_password_hash(password)
        db.execute("UPDATE user SET hash = ? WHERE email = ?", hash, email)
        print("change was a success")
        return render_template("forgot.html")
    return render_template("forgot.html", question=QUESTION)
### hacer el cambio para que en la base de datos el numero de telefono no se numerico sino text###


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("home.html")
    return render_template("home.html")


@app.route("/order", methods=["GET", "POST"])
def order():
    sisa = company()
    hospitalname = str(request.form.get("hospitalname")).capitalize()
    hospitallastname = str(request.form.get("hospitallastname")).capitalize()
    hospitalids = request.form.get("hospitalid")
    hospitalidnumber = request.form.get("hospitalidnumber")
    hospitalemail = request.form.get("hospitalemail")
    hospitalphone = request.form.get("hospitalphone")
    hospitalmonth = request.form.get("hospitalmonth")
    hospitalday = request.form.get("hospitalday")
    hospitalyear = request.form.get("hospitalyear")
    hospitalgender = request.form.get("hospitalgender")
    
    name = str(request.form.get("name")).capitalize()
    lastname = str(request.form.get("lastname")).capitalize()
    ids = request.form.get("id")
    idnumber = request.form.get("idnumber")
    email = request.form.get("email")
    phone = request.form.get("phone")
    month = request.form.get("month")
    day = request.form.get("day")
    year = request.form.get("year")
    gender = request.form.get("gender")
    dat = date.today()
    if request.method == "POST":
        id = session.get("user_id")
        user_id = id
        if sisa == "Bank":
            if not name or not lastname or not email or not phone or not month or not day or not year or not gender or not ids or not idnumber:
                error = "Missing Information"
                return render_template("order.html", gender=GENDER, error=error, ID=ID)
            db.execute("INSERT INTO customers (user_id, name, lastname, id, id_number, email, phone, day, month, year, gender, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, name, lastname, ids, idnumber, email, phone, day, month, year, gender, dat)
            return redirect("/turnos")
        if sisa == "Hospital":
            if not hospitalname or not hospitallastname or not hospitalemail or not hospitalphone or not hospitalmonth or not hospitalday or not hospitalyear or not hospitalgender or not hospitalids or not hospitalidnumber:
                error = "Missing Information"
                return render_template("order.html", gender=GENDER, error=error, ID=ID)
            db.execute("INSERT INTO hospital_customers (user_id, name, lastname, id, id_number, email, phone, day, month, year, gender, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, hospitalname, hospitallastname, hospitalids, hospitalidnumber, hospitalemail, hospitalphone, hospitalday, hospitalmonth, hospitalyear, hospitalgender, dat)
            return redirect("/turnos")
        return redirect("/turnos")
        
    return render_template("order.html", gender=GENDER, ID=ID, sisa=sisa)

@app.route("/turnos", methods=["GET", "POST"])
def turnos():
    sisa = company()
    emergency = request.form.get("emergency")
    service = request.form.get("service")
    urgency = request.form.get("urgency") 
    medical = request.form.get("medical")
    drugs = request.form.get("drugs")
    hospitalhelp = request.form.get("hospitalhelp")
    
    withdrawals = request.form.get("withdrawals")
    advisory = request.form.get("advisory")
    inquiries = request.form.get("inquiries") 
    help = request.form.get("help")
    loans = request.form.get("loans")
    payments = request.form.get("payments")
    dat = date.today()
    
    if request.method == "POST":
        id = session.get("user_id")
        user_id = id
        if emergency:
            print(TURNOS[0])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO emergency (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[0], name, lastname, email, phone, dat)
            emergency_id = db.execute("SELECT emergency_id FROM emergency WHERE user_id = ?", user_id)
            quantity = len(emergency_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM emergency WHERE emergency_id = ?", emergency_id[new_id]["emergency_id"])
            TURNOS[0]= TURNOS[0] + 1
            if TURNOS[0] == 999:
                TURNOS[0] = 1
            return render_template("message.html", turno=turno)
        if service:
            print(TURNOS[1])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO service (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[1], name, lastname, email, phone, dat)
            service_id = db.execute("SELECT service_id FROM service WHERE user_id = ?", user_id)
            quantity = len(service_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM service WHERE service_id = ?", service_id[new_id]["service_id"])
            TURNOS[1]= TURNOS[1] + 1
            if TURNOS[1] == 999:
                TURNOS[1] = 1
            return render_template("message.html", turno=turno)
        if urgency:
            print(TURNOS[2])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO urgency (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[2], name, lastname, email, phone, dat)
            urgency_id = db.execute("SELECT urgency_id FROM urgency WHERE user_id = ?", user_id)
            quantity = len(urgency_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM urgency WHERE urgency_id = ?", urgency_id[new_id]["urgency_id"])
            TURNOS[2]= TURNOS[2] + 1
            if TURNOS[2] == 999:
                TURNOS[2] = 1
            return render_template("message.html", turno=turno)
        if medical:
            print(TURNOS[3])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO medical (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[3], name, lastname, email, phone, dat)
            medical_id = db.execute("SELECT medical_id FROM medical WHERE user_id = ?", user_id)
            quantity = len(medical_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM medical WHERE medical_id = ?", medical_id[new_id]["medical_id"])
            TURNOS[3]= TURNOS[3] + 1
            if TURNOS[3] == 999:
                TURNOS[3] = 1
            return render_template("message.html", turno=turno)
        if drugs:
            print(TURNOS[4])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO drugs (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[4], name, lastname, email, phone, dat)
            drugs_id = db.execute("SELECT drugs_id FROM drugs WHERE user_id = ?", user_id)
            quantity = len(drugs_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM drugs WHERE drugs_id = ?", drugs_id[new_id]["drugs_id"])
            TURNOS[4]= TURNOS[4] + 1
            if TURNOS[4] == 999:
                TURNOS[4] = 1
            return render_template("message.html", turno=turno)
        if hospitalhelp:
            print(TURNOS[5])
            rows = db.execute("SELECT name, lastname, email, phone FROM hospital_customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO hospitalhelp (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[5], name, lastname, email, phone, dat)
            hospitalhelp_id = db.execute("SELECT hospitalhelp_id FROM hospitalhelp WHERE user_id = ?", user_id)
            quantity = len(hospitalhelp_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM hospitalhelp WHERE hospitalhelp_id = ?", hospitalhelp_id[new_id]["hospitalhelp_id"])
            TURNOS[5]= TURNOS[5] + 1
            if TURNOS[5] == 999:
                TURNOS[5] = 1
            return render_template("message.html", turno=turno)
        if withdrawals:
            print(TURNOS[0])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO withdrawals (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[0], name, lastname, email, phone, dat)
            withdrawals_id = db.execute("SELECT withdrawals_id FROM withdrawals WHERE user_id = ?", user_id)
            quantity = len(withdrawals_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM withdrawals WHERE withdrawals_id = ?", withdrawals_id[new_id]["withdrawals_id"])
            TURNOS[0]= TURNOS[0] + 1
            if TURNOS[0] == 999:
                TURNOS[0] = 1
            return render_template("message.html", turno=turno)
        if advisory:
            print(TURNOS[1])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO advisory (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[1], name, lastname, email, phone, dat)
            advisory_id = db.execute("SELECT advisory_id FROM advisory WHERE user_id = ?", user_id)
            quantity = len(advisory_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM advisory WHERE advisory_id = ?", advisory_id[new_id]["advisory_id"])
            TURNOS[1]= TURNOS[1] + 1
            if TURNOS[1] == 999:
                TURNOS[1] = 1
            return render_template("message.html", turno=turno)
        if inquiries:
            print(TURNOS[2])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO inquiries (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[2], name, lastname, email, phone, dat)
            inquiries_id = db.execute("SELECT inquiries_id FROM inquiries WHERE user_id = ?", user_id)
            quantity = len(inquiries_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM inquiries WHERE inquiries_id = ?", inquiries_id[new_id]["inquiries_id"])
            TURNOS[2]= TURNOS[2] + 1
            if TURNOS[2] == 999:
                TURNOS[2] = 1
            return render_template("message.html", turno=turno)
        if help:
            print(TURNOS[3])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO help (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[3], name, lastname, email, phone, dat)
            help_id = db.execute("SELECT help_id FROM help WHERE user_id = ?", user_id)
            quantity = len(help_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM help WHERE help_id = ?", help_id[new_id]["help_id"])
            TURNOS[3]= TURNOS[3] + 1
            if TURNOS[3] == 999:
                TURNOS[3] = 1
            return render_template("message.html", turno=turno)
        if loans:
            print(TURNOS[4])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO loans (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[4], name, lastname, email, phone, dat)
            loans_id = db.execute("SELECT loans_id FROM loans WHERE user_id = ?", user_id)
            quantity = len(loans_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM loans WHERE loans_id = ?", loans_id[new_id]["loans_id"])
            TURNOS[4]= TURNOS[4] + 1
            if TURNOS[4] == 999:
                TURNOS[4] = 1
            return render_template("message.html", turno=turno)
        if payments:
            print(TURNOS[5])
            rows = db.execute("SELECT name, lastname, email, phone FROM customers WHERE user_id = ?", user_id)
            l = len(rows)
            name = rows[l - 1]["name"]
            lastname = rows[l - 1]["lastname"]
            email = rows[l - 1]["email"]
            phone = rows[l - 1]["phone"]
            db.execute("INSERT INTO payments (user_id, turn, name, lastname, email, phone, date) VALUES(?,?,?,?,?,?,?)", user_id, TURNOS[5], name, lastname, email, phone, dat)
            payments_id = db.execute("SELECT payments_id FROM payments WHERE user_id = ?", user_id)
            quantity = len(payments_id)
            new_id = quantity - 1
            turno = db.execute("SELECT turn, name, lastname FROM payments WHERE loans_id = ?", payments_id[new_id]["payments_id"])
            TURNOS[5]= TURNOS[5] + 1
            if TURNOS[5] == 999:
                TURNOS[5] = 1
            return render_template("message.html", turno=turno)
    return render_template("turnos.html", sisa=sisa)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/exit", methods=["GET", "POST"])
def exit():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if request.method == "POST":
        if not email or not password:
            error = "Wrong Credentials!"
            return render_template("exit.html", error=error)
        rows = db.execute("SELECT * FROM user WHERE email = ?", email)
        if rows == []:
            error = "Email was not found!"
            return render_template("exit.html", error=error)
        if email != rows[0]["email"]:
            error = "Email Incorrect!"
            return render_template("exit.html", error=error)
        if not check_password_hash(
            rows[0]["hash"], password
        ):
            error = "passowrd Incorrect!"
            return render_template("exit.html", error=error)
        return redirect("/home")
    return render_template("exit.html")


@app.route("/stats", methods=["GET", "POST"])
def stats():
    id = session.get("user_id")
    user_id = id
    sisa = company()
    m = (request.form.get("month"))
    d = (request.form.get("day"))
    y = (request.form.get("year"))
    m2 = (request.form.get("month2"))
    d2 = (request.form.get("day2"))
    y2 = (request.form.get("year2"))
    if request.method == "POST":
        month = str(m)
        day = str(d)
        year = str(y)
        month2 = str(m2)
        day2 = str(d2)
        year2 = str(y2)
        g = "-"
        date = (year + g + month + g + day)
        date2 = (year2 + g + month2 + g + day2)
        hospitaltotal = db.execute("SELECT COUNT(*) as count FROM hospital_customers WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        emergency = db.execute("SELECT COUNT(*) as count FROM emergency WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        service = db.execute("SELECT COUNT(*) as count FROM service WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        urgency = db.execute("SELECT COUNT(*) as count FROM urgency WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        medical = db.execute("SELECT COUNT(*) as count FROM medical WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        drugs = db.execute("SELECT COUNT(*) as count FROM drugs WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        hospitalhelp = db.execute("SELECT COUNT(*) as count FROM hospitalhelp WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        total = db.execute("SELECT COUNT(*) as count FROM customers WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        withdrawals = db.execute("SELECT COUNT(*) as count FROM withdrawals WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        advisory = db.execute("SELECT COUNT(*) as count FROM advisory WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        inquiries = db.execute("SELECT COUNT(*) as count FROM inquiries WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        help = db.execute("SELECT COUNT(*) as count FROM help WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        loans = db.execute("SELECT COUNT(*) as count FROM loans WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        payments = db.execute("SELECT COUNT(*) as count FROM payments WHERE date BETWEEN ? AND ? AND user_id = ?", date, date2, user_id)
        if request.form.get("hospitaltotal"):
            rows = db.execute("SELECT * FROM hospital_customers WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("emergency"):
            rows = db.execute("SELECT * FROM emergency WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("service"):
            rows = db.execute("SELECT * FROM service WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("urgency"):
            rows = db.execute("SELECT * FROM urgency WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("medical"):
            rows = db.execute("SELECT * FROM medical WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("drugs"):
            rows = db.execute("SELECT * FROM drugs WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("hospitalhelp"):
            rows = db.execute("SELECT * FROM hospitalhelp WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("total"):
            rows = db.execute("SELECT * FROM customers WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("withdrawals"):
            rows = db.execute("SELECT * FROM withdrawals WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("advisory"):
            rows = db.execute("SELECT * FROM advisory WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("inquiries"):
            rows = db.execute("SELECT * FROM inquiries WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("help"):
            rows = db.execute("SELECT * FROM help WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("loans"):
            rows = db.execute("SELECT * FROM loans WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        if request.form.get("payments"):
            rows = db.execute("SELECT * FROM payments WHERE user_id = ?", user_id)
            return render_template("table.html", rows=rows)
        return render_template("stats.html", total=total, withdrawals=withdrawals, advisory=advisory, inquiries=inquiries, help=help, loans=loans, payments=payments, hospitaltotal=hospitaltotal, emergency=emergency, service=service, urgency=urgency, medical=medical, drugs=drugs, hospitalhelp=hospitalhelp, sisa=sisa)
    return render_template("stats.html", sisa=sisa)


@app.route("/profile", methods=["GET","POST"])
def profile(): 
    id = session.get("user_id")
    user_id = id
    email = request.form.get("email")
    size = request.form.get("size")
    rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    if request.method == "POST":
        if request.form.get("email"):
            return redirect("/edit")
        if request.form.get("business"):
            return redirect("/editbusiness")
        if request.form.get("size"):
            return redirect("/editsize")
        if request.form.get("phone"):
            return redirect("/editphone")
        return render_template("edit.html", rows=rows)
    return render_template("profile.html", rows=rows)

@app.route("/edit", methods=["GET","POST"])
def edit():
    id = session.get("user_id")
    user_id = id
    rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    if request.method == "POST":
        newemail = request.form.get("newemail")
        rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        oldemail = rows[0]["email"]
        print(oldemail)
        print(newemail)
        change = db.execute("UPDATE user SET email = ? WHERE email = ? AND id = ?", newemail, oldemail, user_id)
        print(change)
        return redirect("/profile")
    return render_template("edit.html", rows=rows)

@app.route("/editbusiness", methods=["GET","POST"])
def editbusiness():
    id = session.get("user_id")
    user_id = id
    rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    if request.method == "POST":
        newbusiness = request.form.get("newbusiness")
        rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        oldbusiness = rows[0]["business"]
        print(oldbusiness)
        print(newbusiness)
        change = db.execute("UPDATE user SET business = ? WHERE business = ? AND id = ?", newbusiness, oldbusiness, user_id)
        print(change)
        return redirect("/profile")
    return render_template("editbusiness.html", rows=rows, options=OPTIONS)

@app.route("/editsize", methods=["GET","POST"])
def editsize():
    id = session.get("user_id")
    user_id = id
    rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    if request.method == "POST":
        newsize = request.form.get("newsize")
        rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        oldsize = rows[0]["size"]
        print(oldsize)
        print(newsize)
        change = db.execute("UPDATE user SET size = ? WHERE size = ? AND id = ?", newsize, oldsize, user_id)
        print(change)
        return redirect("/profile")
    return render_template("editsize.html", rows=rows, size=SIZE)
    
@app.route("/editphone", methods=["GET","POST"])
def editphone():
    id = session.get("user_id")
    user_id = id
    rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    if request.method == "POST":
        newphone = request.form.get("newphone")
        rows = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        oldphone = rows[0]["phone"]
        print(oldphone)
        print(newphone)
        change = db.execute("UPDATE user SET phone = ? WHERE phone = ? AND id = ?", newphone, oldphone, user_id)
        print(change)
        return redirect("/profile")
    return render_template("editphone.html", rows=rows)

    
@app.route("/staff", methods=["GET", "POST"])
def staff():
    id = session.get("user_id")
    user_id = id
    sisa = company()
    staf = "Ok"
    if request.method == "POST":    
        staff.spot = request.form.get("cubicle")
        staff.queu = request.form.get("queu")
        if staff.spot == "1":
            staff.spot.spot1 = 1
            staff.queu.spot1 = staff.queu
        if staff.spot == "2":
            staff.spot.spot2 = 2
            staff.queu.spot2 = staff.queu
        if staff.spot == "3":
            staff.spot.spot3 = 3
            staff.queu.spot3 = staff.queu
        if staff.spot == "4":
            staff.spot.spot4 = 4
            staff.queu.spot4 = staff.queu
        if staff.spot == "5":
            staff.spot.spot5 = 5
            staff.queu.spot5 = staff.queu
        if staff.spot == "6":
            staff.spot.spot6 = 6
            staff.queu.spot6 = staff.queu
        if staff.spot == "7":
            staff.spot.spot7 = 7
            staff.queu.spot7 = staff.queu
        if staff.spot == "8":
            staff.spot.spot8 = 8
            staff.queu.spot8 = staff.queu
        if staff.spot == "9":
            staff.spot.spot9 = 9
            staff.queu.spot9 = staff.queu
        if staff.spot == "10":
            staff.spot.spot10 = 10
            staff.queu.spot10 = staff.queu
        return redirect("/numero")
    return render_template("staff.html", cubicle=CUBICLE, sisa=sisa, bank=BANK, hospital=HOSPITAL)
    
@app.route("/numero", methods=["GET", "POST"])
def numero():
    if request.method == "POST":
        if staff.spot == "1":
            staff.spot.spot1
            staff.queu.spot1
        if staff.spot == "2":
            staff.spot.spot2 = 2
            staff.queu.spot2 = staff.queu
        if staff.spot == "3":
            staff.spot.spot3 = 3
            staff.queu.spot3 = staff.queu
        if staff.spot == "4":
            staff.spot.spot4
            staff.queu.spot4
        if staff.spot == "5":
            staff.spot.spot5 = 5
            staff.queu.spot5 = staff.queu
        if staff.spot == "6":
            staff.spot.spot6 = 6
            staff.queu.spot6 = staff.queu
        if staff.spot == "7":
            staff.spot.spot7 = 7
            staff.queu.spot7 = staff.queu
        if staff.spot == "8":
            staff.spot.spot8 = 8
            staff.queu.spot8 = staff.queu
        if staff.spot == "9":
            staff.spot.spot9 = 9
            staff.queu.spot9 = staff.queu
        if staff.spot == "10":
            staff.spot.spot10 = 10
            staff.queu.spot10 = staff.queu
        spot = int(staff.spot)
        queu = staff.queu
        print(spot)
        print(queu)
        next = request.form.get("next")
        if next:
            STAFFTURNOS[spot-1] = STAFFTURNOS[spot-1] + 1
            numero.tunos = STAFFTURNOS[spot-1]
            if STAFFTURNOS[spot-1] == 999:
                STAFFTURNOS[spot-1] = 0
            print(STAFFTURNOS[spot-1])
        return render_template("numero.html", turno=STAFFTURNOS[spot-1], spot=spot, queu=queu)
    return render_template("numero.html")

@app.route("/screen", methods=["GET", "POST"])
def screen():
    return render_template("screen.html", spot1=STAFFTURNOS[0], spot2=STAFFTURNOS[1], spot3=STAFFTURNOS[2], spot4=STAFFTURNOS[3], spot5=STAFFTURNOS[4], spot6=STAFFTURNOS[5], spot7=STAFFTURNOS[6], spot8=STAFFTURNOS[7], spot9=STAFFTURNOS[8], spot10=STAFFTURNOS[9], spot11=STAFFTURNOS[10], spot12=STAFFTURNOS[11], spot13=STAFFTURNOS[12], spot14=STAFFTURNOS[13], spot15=STAFFTURNOS[14], spot16=STAFFTURNOS[15], spot17=STAFFTURNOS[16], spot18=STAFFTURNOS[17], spot19=STAFFTURNOS[18], spot20=STAFFTURNOS[19])
    
    
    
###missing: we need that after the staff choose their spot and queu, they can click on next and the next cx information and turn reflected in the screen###
### menu/staff to make the part of the staff that say next turn and alll that shit ###