#Pass information from Backend of Flask to the frontend of HTML template
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hellothisismysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_table.sqlite3' # "users_table" here is the name of the table that you're gonna be referencing 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=3) # store our permanent session data for 3 minutes


db = SQLAlchemy(app) # SQLAlchemy makes it easier to save information because we can write all our database stuff in python code rather than writing SQL queries

class users_table(db.Model): # The columns represent pieces of information；Rows represent in ；Rows represent individual items
    _id = db.Column("id",db.Integer, primary_key=True) # id will be automatically be created for us because it's a primary key
    name = db.Column(db.String(100)) # 100 here is the maximum length of the string that we want to store(100 characters)
    email = db.Column(db.String(100)) # string也可以改成integer/float/boolean

    def __init__(self,name,email): # We want to store users and each users has a name and an email (these 2 are what we need every time we define a new user object)(the init method will take the variables that we need to create a new object)
        self.name = name
        self.email = email


#@app.route("/<name>")
#def home(name):
    #return "Hello! This is the main page <h1>HELLO<h1>"
    #return render_template("index.html", content=name, r=2)
    #return render_template("index.html",content=["Tim","Joe","Bill"])
'''@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))'''

'''@app.route("/")
def home():
    return render_template("index.html",content="Testing")'''

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html",values=users_table.query.all())


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True #used to define this specific session as a permanent session which means it's gonna last as long as we define up there 
        user = request.form["nm"]
        session["user"] = user

        found_user = users_table.query.filter_by(name=user).first()
        if found_user: # When an user types his name, we'll check if this user is already exist. If not then we'll create one
            session["email"] = found_user.email
        else:
            usr = users_table(user, "")
            db.session.add(usr) # add this user model to our database
            db.session.commit()

        flash("Login Succesful!")
        #return redirect(url_for("user",usr=user))
        return redirect(url_for("user"))
    else:
        if "user" in session: #代表若已經是signed in的狀態
            flash("Already Logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")



'''@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"'''

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST": 
            email = request.form["email"] # grab that email from the email field
            session["email"] = email # store it in the session
        
            found_user = users_table.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit() # next time we login this will be saved

            flash("Email was saved!")
        else: # if it's a GET request
            if "email" in session:
                email = session["email"] # get the email from the session

        #return f"<h1>{user}</h1>"
        #return render_template("User.html", user=user)
        return render_template("User.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    #if "user" in session:
        #user = session["user"]
    flash("You have been logged out!", "info")
    session.pop("user",None) #remove the user data from my session 
    session.pop("email",None)
    return redirect(url_for("login"))


@app.route("/WhatisNew")
def WhatisNew():
    return render_template("new.html")

if __name__ == "__main__":
    db.create_all() # create the database above if it hasn't already exist in our program
    app.run(debug=True)
