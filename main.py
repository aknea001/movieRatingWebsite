from flask import Flask, request, render_template, redirect, flash, session, url_for
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASKPASSWD")
app.jinja_env.filters["zip"] = zip

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
        return redirect("/login", code=302)
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

            if "url" in session:
                toRedirect = session["url"]
                session.pop("url")

                return redirect(toRedirect)
            else:
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

        query = "SELECT title, id FROM movies WHERE title LIKE %s OR title LIKE CONCAT('the ', %s)"
        placeholders = [f"{searchQuery}%"] * 2
        cursor.execute(query, placeholders)
        result = cursor.fetchall()

        titles = [row[0] for row in result]
        ratings = [row[1] for row in result]
        #print(titles)
        #print(ratings)

        return render_template("search.html", titles=titles, movieID=ratings, searched=searchQuery)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

@app.route("/title/<titleID>")
def moviePage(titleID):
    db = None

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        query = "SELECT movies.title, movies.genre, GROUP_CONCAT(ratings.rating ORDER BY ratings.rating ASC)\
            AS allRatings FROM movies INNER JOIN ratings ON ratings.movieID = movies.id\
            WHERE ratings.movieID = %s GROUP BY movies.id, movies.title, movies.genre;"
        cursor.execute(query, (titleID, ))
        info = cursor.fetchone()

        if info == None:
            query = "SELECT title, genre FROM movies WHERE id = %s"
            cursor.execute(query, (titleID, ))
            info = cursor.fetchone()

        try:
            ratings = info[2]
            ratingsList = [int(rating) for rating in info[2].split(",")]
            average = sum(ratingsList) / len(ratingsList)
            averageRounded = round(average, 1)
            # print(ratings)
        except IndexError:
            ratings = "Not rated yet"
            averageRounded = "no average"

        return render_template("title.html", title=info[0], genre=info[1], ratings=ratings, average=averageRounded, movieID=titleID)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

@app.route("/title/<titleID>", methods=["POST"])
def rateForm(titleID):
    rating = request.form["rating"]

    db = None

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        if "userID" in session:
            query = "INSERT INTO ratings (movieID, rating, userID) VALUES (%s, %s, %s)"
            cursor.execute(query, (titleID, rating, session["userID"])) # usin userID 1 just for testin, change after (gotta check if logged in to rate)
            db.commit()

            flash("Successfully sent data..")
            return redirect(url_for("moviePage", titleID=titleID))
        else:
            flash("You have to be logged in..")
            session["url"] = url_for("moviePage", titleID=titleID)
            return redirect(url_for("login"))
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

@app.route("/submit_movie")
def subMovie():
    return render_template("addMovie.html")

@app.route("/submit_movie", methods=["POST"])
def submitMovieForm():
    title = request.form["title"]
    genre = request.form["genre"]

    db = None

    try:
        db = mysql.connector.connect(**sqlConfig)
        cursor = db.cursor(buffered=True)

        query = "INSERT INTO movies (title, genre) VALUES (%s, %s)"
        cursor.execute(query, (title, genre))
        db.commit()

        flash("Successfully sent data..")
        return redirect("/", code=302)
    except mysql.connector.Error as e:
        return f"ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")