from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "abcd123"   # Change this to anything random

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="db4free.net",
        user="prapti",
        password="123456789",
        database="anuradha"
    )


# -----------------------------
# HOME / LOGIN PAGE (GET only)
# -----------------------------
@app.route('/')
def home():
    return redirect(url_for("login"))


# -----------------------------
# LOGIN ROUTE
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        mydb = get_db_connection()
        cursor = mydb.cursor()

        cursor.execute(
            "SELECT * FROM LoginDetails WHERE Name = %s AND Password = %s",
            (username, password)
        )
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['name'] = account[1]

            msg = "Logged in Successfully"
            return render_template("welcome.html", msg=msg, name=session['name'])

        else:
            msg = "Incorrect Credentials. Please try again."
            return render_template("login.html", msg=msg)

    return render_template("login.html", msg=msg)


# -----------------------------
# REGISTRATION ROUTE
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        mydb = get_db_connection()
        cursor = mydb.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM LoginDetails WHERE Name=%s", (username,))
        existing = cursor.fetchone()

        if existing:
            msg = "Username already exists. Try a different one."
            return render_template("register.html", msg=msg)

        # Insert new user
        cursor.execute(
            "INSERT INTO LoginDetails (Name, Password) VALUES (%s, %s)",
            (username, password)
        )
        mydb.commit()

        msg = "Registration successful! Please login."
        return redirect(url_for("login"))

    return render_template("register.html", msg=msg)


# -----------------------------
# PROTECTED WELCOME PAGE
# -----------------------------
@app.route('/welcome')
def welcome():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    return render_template(
        "welcome.html",
        msg="You are successfully logged in",
        name=session["name"]
    )


# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
