from flask import Flask, request, render_template, redirect, flash, session
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

    db = None # Gotta declare db var before try in case it fails

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        query = "INSERT INTO users (email, passwd, country) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, passwd, country))
        db.commit()

        flash("Successfully sent data..")
        return redirect("/", code=302)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginForm():
    email = request.form["email"]
    passwd = request.form["passwd"]

    db = None

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        query = "SELECT * FROM users WHERE email = %s AND passwd = %s"
        cursor.execute(query, (email, passwd))
        user = cursor.fetchone()

        if user:
            session["userID"] = user[0]
            #print(f"ID: {session['userID']}")

            flash("Successfully logged in..")
            return redirect("/", code=302)
        else:
            flash("Invalid email or password..")
            return redirect("/login", code=302)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out..")
    return redirect("/", code=302)

@app.route("/search", methods=["POST"])
def search():
    searchQuery = request.form["searchQuery"]

    db = None

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        query = "SELECT title FROM movies WHERE title LIKE 'sh%'"
        cursor.execute(query)
        result = cursor.fetchall()

        # Convert result to a plain text response
        titles = [row[0] for row in result]  # Extract titles from result

        return render_template("search.html", titles=titles)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    app.run(debug=True)