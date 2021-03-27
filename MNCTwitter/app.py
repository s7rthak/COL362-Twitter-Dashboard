from flask import Flask, render_template, redirect, url_for, request
import sys
from database import *
from images import *


app = Flask(__name__)

# **************** APPLICATION ENDPIONTS **************** 

user = None

# test endpoint
@app.route("/test")
def test():
	return render_template("test.html")


# template endpoint
@app.route("/template")
def template():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("template.html", usr = user, image = image)

# home url endpoint
@app.route("/")
def home():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("home.html", usr = user, image = image)

# post_tweet endpoint
@app.route("/post_tweet")
def post_tweet():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("post_tweet.html", usr = user, image = image)

# my_tweets endpoint
@app.route("/my_tweets")
def my_tweets():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("my_tweets.html", usr = user, image = image)

# users endpoint
@app.route("/users")
def users():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("users.html", usr = user, image = image)

# read_tweets endpoint
# @app.route("/read_tweets")
# def read_tweets():
# 	global user
# 	if not user:
# 		return redirect(url_for("login"))

# 	return render_template("read_tweets.html", usr = user, image = image)

@app.route("/read_tweets", methods = ["GET", "POST"])
def read_tweets():
	global user
	if not user:
		return redirect(url_for("login"))
	elif request.method == "GET":
		return render_template("read_tweets.html", usr = user, image = image, posting=None)
	else:
		userid = request.form["userid"]
		companyname = request.form["company"]
		mylist = [(1, "my tweet 1"), (20, "mytweet 2")]
		return render_template("read_tweets.html", usr = user, image = image, posting=1, mylist = mylist, mylen = len(mylist))


# network_analysis endpoint
@app.route("/network_analysis")
def network_analysis():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("network_analysis.html", usr = user, image = image)

# company_analysis endpoint
@app.route("/company_analysis")
def company_analysis():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("company_analysis.html", usr = user, image = image)

# account endpoint
@app.route("/account")
def account():
	global user
	if not user:
		return redirect(url_for("login"))

	return render_template("account.html", usr = user, image = image)

# logout endpoint
@app.route("/logout")
def logout():
	global user
	user = None
	return redirect(url_for("login"))


# login endpoint
@app.route("/login", methods = ["GET", "POST"])
def login():
	global user
	if user:
		return redirect(url_for("home"))

	error = None
	if request.method == "POST":
		# Login
		if check_user(request.form["username"], request.form["password"]):
			user = request.form["username"]
			return redirect(url_for("home"))
		else:
			error = "Invalid credentials. Please try again."

	return render_template("login.html", error = error, image = image)


# signup endopint
@app.route("/signup", methods = ["GET", "POST"])
def signup():
	global user
	if user:
		return redirect(url_for("home"))

	error = None
	if request.method == "POST":
		error = check_new_user(request.form["username"], request.form["password"], request.form["repassword"])

		# Sign Up
		if not error:
			user = request.form["username"]
			return redirect(url_for("home"))

	return render_template("signup.html", error = error, image = image)

# terms_and_privacy endopint
@app.route("/terms_and_privacy")
def terms_and_privacy():
	return render_template("terms_and_privacy.html", image = image)


# **************** MAIN ****************

if __name__ == "__main__":
	# connect to the PostgreSQL server
	connect(host="localhost", database=sys.argv[1], user="dbms_project", password="dbms_project")

	# Starting the server
	app.run(debug = True) # Debug mode will give us the bugger that we can use in a browser and auto-reload function

	# closing the server
	close()

