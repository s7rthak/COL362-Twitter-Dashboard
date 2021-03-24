from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


# Main url endpoint
@app.route("/")
def home():
	return "Hello, world!"


# Welcome endpoint
@app.route("/welcome")
def welcome():
	return render_template("welcome.html")


# Login endpoint
@app.route("/login", methods = ["GET", "POST"]) # GET method is by default, other methods need to be added explicitly, POST is used so that users can post username & password
def login():
	error = None
	if request.method == "POST":
		if request.form["username"] != "admin" or request.form["password"] != "admin":
			error = "Invalid credentials. Please try again."
		else:
			return redirect(url_for("home"))


	return render_template("login.html", error=error)

if __name__ == "__main__":
	app.run(debug = True) # Debug mode will give us the bugger that we can use in a browser and auto-reload function
