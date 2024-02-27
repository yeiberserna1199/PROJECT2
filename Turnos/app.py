
import sys
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functools import wraps
from itsdangerous import URLSafeTimedSerializer as Serializer

app = Flask(__name__)

OPTIONS = [
    "Restaurant",
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
###se mantiene asi por el momento porque aun no he hecho el homepage luego de subcribirse ni loguearse.### 

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
    return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION)
###se mantiene asi por el momento porque aun no he hecho el homepage luego de subcribirse ni loguearse.### 

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
        print(rows[0]["email"])
        print(email)
        print(rows[0]["phone"])
        print(phone)
        print(rows[0]["security"])
        print(security)
        print(rows[0]["answer"])
        print(answer)
        
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