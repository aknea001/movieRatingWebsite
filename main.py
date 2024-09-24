from flask import Flask, request, render_template, redirect, flash
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASKPASSWD")

sqlConfig = {
    "host": "100.94.183.127",
    "user": "keali",
    "password": os.getenv("SQLPASSWD"),
    "database": "movieRating"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def registerForm():
    email = request.form["email"]
    passwd = request.form["passwd"]
    country = request.form["country"]

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor()

        query = "INSERT INTO users (email, passwd, country) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, passwd, country))
        db.commit()

        flash("Successfully sent data..")
        return redirect("/", code=302)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginForm():
    email = request.form["email"]
    passwd = request.form["passwd"]

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor()

        query = "SELECT * FROM users WHERE email = %s AND passwd = %s"
        cursor.execute(query, (email, passwd))
        user = cursor.fetchone()

        if user:
            flash("Successfully logged in..")
            return redirect("/", code=302)
        else:
            flash("Invalid email or password..")
            return redirect("/login", code=302)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    app.run(debug=True)