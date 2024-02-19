
import sqlite3
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



connection = sqlite3.connect("turnos.db")
cursor = connection.cursor()

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
            return render_template("homepage.html")
    return render_template("homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return render_template("register.html")
    return render_template("register.html", options=OPTIONS, size=SIZE, question=QUESTION)