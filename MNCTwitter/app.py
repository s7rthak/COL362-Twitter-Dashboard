from flask import Flask, render_template, redirect, url_for, request
import sys
from database import *
from images import *


app = Flask(__name__)

# **************** APPLICATION ENDPIONTS **************** 

user_id = None
user_name = ""

# test endpoint
@app.route("/test", methods = ["GET", "POST"])
def test():
	return render_template("test.html", image = image)

# check endpoint
@app.route("/check")
def check():
	check_db()
	return redirect(url_for("login"))


# message endpoint
@app.route("/message")
def message():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	msg = request.args.get('msg')
	return render_template("message.html", usr = user_name, usr_id = user_id, image = image, message = msg)

# template endpoint
@app.route("/template")
def template():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	return render_template("template.html", usr = user_name, usr_id = user_id, image = image)

# home url endpoint
@app.route("/", methods = ["GET", "POST"])
def home():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		hashtag = ""
		for key in request.form:
			hashtag = key

		tweets_info = [["Showing tweets with popular hash: ", hashtag]]
		tweets_list = get_popular_hash_tweets_db(hashtag)
		return render_template("read_tweets.html", usr = user_name, usr_id = user_id, image = image, tweets_info = tweets_info, tweets_list = tweets_list, tweets_num = len(tweets_list))

	hashes = get_popular_hashes_db()

	return render_template("home.html", usr = user_name, usr_id = user_id, image = image, hashes = hashes)

# post_tweet endpoint
@app.route("/post_tweet", methods = ["GET", "POST"])
def post_tweet():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))


	if request.method == "POST":
		# Companies ------
		company_tickers = request.form.getlist("companies_to_show")
		if "ALL" in request.form.getlist("companies_to_show"):
			company_tickers = ['AAPL', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']
		if company_tickers == []:
			return render_template("post_tweet.html", usr = user_name, usr_id = user_id, image = image, error = "Select at least one company")

		# post new tweet
		post_tweet_db(user_id, request.form["body"], company_tickers)

		return redirect(url_for("message", msg = "Tweet Posted."))

	return render_template("post_tweet.html", usr = user_name, usr_id = user_id, image = image)

# my_tweets endpoint
@app.route("/my_tweets", methods = ["GET", "POST"])
def my_tweets():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		
		# Companies ------
		company_tickers = request.form.getlist("companies_to_show")
		if "ALL" in request.form.getlist("companies_to_show"):
			company_tickers = ['AAPL', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']
		company_names = list(map(get_company_name_db, company_tickers))

		# Users ------
		user_ids = [user_id]

		# Hashes ------
		hashes = []
		include_hashes = "include_hashes" in request.form
		for hashtag_ in request.form["hashes"].split():
			for hashtag in hashtag_.split("#"):
				if len(hashtag.strip()):
					hashes.append(hashtag)
		if not include_hashes:
			hashes = []

		# Time ------
		hour_num = {"Past hour": 1, "Past day": 24, "Past six monthes": 4380, "Past year": 8760 , "Past two years": 17520 , "Past five years": 43800, "All time": 87600}
		one_hour = 3600
		time_range = one_hour * hour_num[request.form["time"]]

		# Order ------
		order = {"Most recent first": "post_date", "Most liked first": "like_num", "Most retweeted first": "retweet_num", "Most reported first": "report_num", "Most commented on first": "comment_num"}
		order_by = order[request.form["order"]]
		
		# tweet_info
		tweets_info = [["Tweets from companies: ", ""], ["Posted in: ", ""], ["In order: ", ""]]
		tweets_info[0][1] += ", ".join(company_names)
		tweets_info[1][1] += request.form["time"]
		tweets_info[2][1] += request.form["order"]
		
		# Getting tweets ------
		tweets_list = []
		if include_hashes:
			tweets_list = get_hash_tweets_db(user_ids, company_tickers, hashes, time_range, order_by)
		else:
			tweets_list = get_tweets_db(user_ids, company_tickers, time_range, order_by)

		return render_template("my_tweets.html", usr = user_name, usr_id = user_id, image = image, tweets_info = tweets_info, tweets_list = tweets_list, tweets_num = len(tweets_list))

	return render_template("my_tweets.html", usr = user_name, usr_id = user_id, image = image)

listing_users = []

# users endpoint
@app.route("/users", methods = ["GET", "POST"])
def users():
	listing_info = request.args.get('listing_info')

	print("*" * 100, listing_info, listing_users)

	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		if request.form.get("RESET"):
			return redirect(url_for("users"))
		
		# Users ------
		user_ids = set()
		
		users_to_show = []
		for user_to_show in request.form.getlist("users_to_show"):
			if user_to_show == "All":
				users_to_show = ["All users"]
				user_ids = get_all_user_ids_db()
				break
			elif user_to_show == "Popular users":
				users_to_show.append(user_to_show)
				user_ids = user_ids.union(set(get_popular_users_db()))
			elif user_to_show == "Users I follow":
				users_to_show.append("Users you follow")
				user_ids = user_ids.union(set(get_users_followed_by_db(user_id)))
			elif user_to_show == "My followers":
				users_to_show.append("Your followers")
				user_ids = user_ids.union(set(get_followers_db(user_id)))
			elif user_to_show == "Me":
				users_to_show.append("You")
				user_ids = user_ids.union(set([user_id]))
			elif user_to_show == "__other_option__":
				for others in request.form.getlist("users_to_show.others"):
					others_list = others.split()
					other_ids = list(map(get_user_id_db, others_list))
					# Adding non-None ids to list
					for this_user_name in others.split():
						this_user_id = get_user_id_db(this_user_name)
						if this_user_id:
							user_ids.add(this_user_id)
							users_to_show.append(this_user_name)

		user_ids = list(user_ids)
		users_list = [(this_user_id, get_user_name_db(this_user_id)) for this_user_id in user_ids]
		users_info = " ".join(users_to_show)

		return render_template("users.html", usr = user_name, usr_id = user_id, image = image, users_info = users_info, users_list = users_list, users_num = len(users_list))

	# global listing_info, listing_users
	if listing_info:
		return render_template("users.html", usr = user_name, usr_id = user_id, image = image, users_info = listing_info, users_list = listing_users, users_num = len(listing_users))

	return render_template("users.html", usr = user_name, usr_id = user_id, image = image)

# user endpoint
@app.route("/user:<user_id_page>", methods = ["GET", "POST"])
def user(user_id_page):
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if not check_available_user_db(user_id):
		return redirect(url_for("message", msg = "This user is not available."))

	common_follow_list = get_common_follow_list_db(user_id, user_id_page)
	common_follow_num = len(common_follow_list)
	common_follower_list = get_common_follower_list_db(user_id, user_id_page)
	common_follower_num = len(common_follower_list)

	# user_info = 0: user_id, 1: user_name, 2: password, 3: tweet_num, 4: follower_num, 5: follow_num, 6: comment_num, 7: retweet_num, 8: like_num, 9: report_num
	limit = 10
	user_info = get_user_info_db(user_id_page)
	user_tweets = get_user_tweets_db(user_id_page)
	is_popular = get_is_popular_db(user_id_page)
	follow_list = get_users_followed_by_limit_db(user_id_page, limit)
	follower_list = get_followers_limit_db(user_id_page, limit)
	user_page = user_id == int(user_id_page)
	user_follows_user_page = user_id in [follower[0] for follower in follower_list]

	mutual_info = {"common_follow_num" : common_follow_num, "common_follow_list" : common_follow_list[:10], "common_follower_num" : common_follower_num, "common_follower_list" : common_follower_list[:10]}

	if request.method == "POST":
		global listing_users
		if request.form.get("ACCOUNT SETTINGS"):
			return redirect(url_for("account"))
		elif request.form.get("UNFOLLOW"):
			delete_follow_db(user_id_page, user_id)
			return redirect(url_for("user", user_id_page = user_id_page))
		elif request.form.get("FOLLOW"):
			add_follow_db(user_id_page, user_id)
			return redirect(url_for("user", user_id_page = user_id_page))
		elif request.form.get("SEE ALL FOLLOWS"):
			listing_info = user_info[1] + " follows"
			follow_num = user_info[5]
			listing_users = tuple(get_users_followed_by_limit_db(user_id_page, follow_num))
			return redirect(url_for("users", listing_info = listing_info, listing_users = listing_users))
		elif request.form.get("SEE ALL FOLLOWERS"):
			listing_info = user_info[1] + "'s followers"
			follower_num = user_info[4]
			listing_users = tuple(get_followers_limit_db(user_id_page, follower_num))
			return redirect(url_for("users", listing_info = listing_info, listing_users = listing_users))
		elif request.form.get("SEE ALL COMMON FOLLOWS"):
			listing_info = "Both you and " + user_info[1] + " follow"
			listing_users = tuple(common_follow_list)
			return redirect(url_for("users", listing_info = listing_info, listing_users = listing_users))
		elif request.form.get("SEE ALL MUTUAL FOLLOWERS"):
			listing_info = "Your mutual followers with " + user_info[1]
			listing_users = tuple(common_follower_list)
			return redirect(url_for("users", listing_info = listing_info, listing_users = listing_users))

	return render_template("user.html", usr = user_name, usr_id = user_id, image = image, user_page = user_page, user_info = user_info, user_tweets = user_tweets, tweets_num = len(user_tweets), is_popular = is_popular, follow_list = follow_list, follower_list = follower_list, user_follows_user_page = user_follows_user_page, mutual_info = mutual_info)

# read_tweets endpoint
@app.route("/read_tweets", methods = ["GET", "POST"])
def read_tweets():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":

		if (request.form.get("Read Most Popular Tweets")):
			tweets_info = [["Showing most popular tweets of all time", ""]]
			tweets_list = get_popular_tweets_db()
			return render_template("read_tweets.html", usr = user_name, usr_id = user_id, image = image, tweets_info = tweets_info, tweets_list = tweets_list, tweets_num = len(tweets_list))

		
		# Companies ------
		company_tickers = request.form.getlist("companies_to_show")
		if "ALL" in request.form.getlist("companies_to_show"):
			company_tickers = ['AAPL', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']
		company_names = list(map(get_company_name_db, company_tickers))

		# Users ------
		user_ids = set()
		all_users = False
		
		users_to_show = []
		for user_to_show in request.form.getlist("users_to_show"):
			if user_to_show == "All":
				all_users = True
				users_to_show = ["All users"]
				break
			elif user_to_show == "Popular users":
				users_to_show.append(user_to_show)
				user_ids = user_ids.union(set(get_popular_users_db()))
			elif user_to_show == "Users I follow":
				users_to_show.append("Users you follow")
				user_ids = user_ids.union(set(get_users_followed_by_db(user_id)))
			elif user_to_show == "My followers":
				users_to_show.append("Your followers")
				user_ids = user_ids.union(set(get_followers_db(user_id)))
			elif user_to_show == "Me":
				users_to_show.append("You")
				user_ids = user_ids.union(set([user_id]))
			elif user_to_show == "__other_option__":
				for others in request.form.getlist("users_to_show.others"):
					others_list = others.split()
					other_ids = list(map(get_user_id_db, others_list))
					# Adding non-None ids to list
					for this_user_name in others.split():
						this_user_id = get_user_id_db(this_user_name)
						if this_user_id:
							user_ids.add(this_user_id)
							users_to_show.append(this_user_name)

		user_ids = list(user_ids)

		# Hashes ------
		hashes = []
		include_hashes = "include_hashes" in request.form
		for hashtag_ in request.form["hashes"].split():
			for hashtag in hashtag_.split("#"):
				if len(hashtag.strip()):
					hashes.append(hashtag)
		if not include_hashes:
			hashes = []


		# Time ------
		hour_num = {"Past hour": 1, "Past day": 24, "Past six monthes": 4380, "Past year": 8760 , "Past two years": 17520 , "Past five years": 43800, "All time": 87600}
		one_hour = 3600
		time_range = one_hour * hour_num[request.form["time"]]

		# Order ------
		order = {"Most recent first": "post_date", "Most liked first": "like_num", "Most retweeted first": "retweet_num", "Most reported first": "report_num", "Most commented on first": "comment_num"}
		order_by = order[request.form["order"]]
		
		# tweet_info
		tweets_info = [["Tweets from companies: ", ""], ["By users: ", ""], ["Posted in: ", ""], ["In order: ", ""]]
		tweets_info[0][1] += ", ".join(company_names)
		tweets_info[1][1] += ", ".join(users_to_show)
		tweets_info[2][1] += request.form["time"]
		tweets_info[3][1] += request.form["order"]

		if include_hashes:
			tweets_info.append(["Showing tweets with hashtags: ", ", ".join(hashes)])
		
		# Getting tweets ------
		tweets_list = []
		if all_users and include_hashes:
			tweets_list = get_all_user_hash_tweets_db(company_tickers, hashes, time_range, order_by)
		elif all_users:
			tweets_list = get_all_user_tweets_db(company_tickers, time_range, order_by)
		elif include_hashes:
			tweets_list = get_hash_tweets_db(user_ids, company_tickers, hashes, time_range, order_by)
		else:
			tweets_list = get_tweets_db(user_ids, company_tickers, time_range, order_by)

		return render_template("read_tweets.html", usr = user_name, usr_id = user_id, image = image, tweets_info = tweets_info, tweets_list = tweets_list, tweets_num = len(tweets_list))

	return render_template("read_tweets.html", usr = user_name, usr_id = user_id, image = image)

# read_tweets endpoint
@app.route("/tweet:<tweet_id>", methods = ["GET", "POST"])
def tweet(tweet_id):
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if not check_available_tweet_db(tweet_id):
		return redirect(url_for("message", msg = "This tweet is not available."))

	if request.method == "POST":
		if request.form.get("LIKE"):
			add_like_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("UNDO LIKE"):
			delete_like_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("RETWEET"):
			add_retweet_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("UNDO RETWEET"):
			delete_retweet_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("REPORT"):
			add_report_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("UNDO REPORT"):
			delete_report_db(user_id, tweet_id)
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("DEL"):
			delete_tweet_db(tweet_id)
			return redirect(url_for("message", msg = "Tweet Deleted."))
		elif request.form.get("COMMENT"):
			add_comment_db(user_id, tweet_id, request.form["comment"])
			return redirect(url_for("tweet", tweet_id = tweet_id))
		elif request.form.get("DELETECOMMENT"):
			delete_comment_db(int(request.form["DELETECOMMENT"]))
			return redirect(url_for("tweet", tweet_id = tweet_id))

	# tweet_info = 0: tweet_id, 1: writer_id, 2: user_name, 3: body, 4: post_date, 5: tweet.comment_num, 6: tweet.retweet_num, 7: tweet.like_num, 8: tweet.report_num, 9: is_retweet, 10: original_tweet_id
	tweet_info = get_tweet_db(tweet_id)

	user_tweet = tweet_info[1] == user_id
	liked = check_like_db(user_id, tweet_id)
	retweeted = check_retweet_db(user_id, tweet_id)
	reported = check_report_db(user_id, tweet_id)
	comment_list = get_comment_list_db(user_id, tweet_id)

	return render_template("tweet.html", usr = user_name, usr_id = user_id, image = image, tweet_id = tweet_id, tweet_info = tweet_info, user_tweet = user_tweet, liked = liked, retweeted = retweeted, reported = reported, comment_list = comment_list)

	
# network_analysis endpoint
@app.route("/network_analysis", methods = ["GET", "POST"])
def network_analysis():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		
		# Users ------
		user_ids = []
		
		user_to_show = request.form["users_to_show"]
		if user_to_show == "People who have observed you":
			user_ids = list(get_observers_db(user_id))
		elif user_to_show == "Users you may know":
			user_ids = list(get_recommendations_db(user_id))
		elif user_to_show == "Users your interests match with":
			user_ids = list(get_matching_db(user_id))
		
		users_list = [(this_user_id, get_user_name_db(this_user_id)) for this_user_id in user_ids]
		users_info = user_to_show
		# print(users_list)
		return render_template("network_analysis.html", usr = user_name, usr_id = user_id, image = image, users_info = users_info, users_list = users_list, users_num = len(users_list))
	return render_template("network_analysis.html", usr = user_name, usr_id = user_id, image = image)

# company_analysis endpoint
@app.route("/company_analysis", methods = ["GET", "POST"])
def company_analysis():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		companycode = request.form["companies_to_show"]
		topfans = get_topfans_db(companycode)
		totallikes = get_totallikes_db(companycode)
		mosttrending = get_mosttrending_db(companycode)
		mosttweets = get_maxtweets_db(companycode)
		longest_streak = get_longest_streak_db(companycode)
		users_list = [(this_user_id, get_user_name_db(this_user_id)) for this_user_id in topfans]
		
		return render_template("company_analysis.html", usr = user_name, usr_id = user_id, image = image, users_info=get_company_name_db(companycode), users_list=users_list, users_num=len(users_list), totallikes=totallikes, mosttrending=mosttrending, mosttweets=mosttweets, longest_streak = longest_streak)
	return render_template("company_analysis.html", usr = user_name, usr_id = user_id, image = image)

# account endpoint
@app.route("/account", methods = ["GET", "POST"])
def account():
	global user_id, user_name
	if not user_id:
		return redirect(url_for("login"))

	if request.method == "POST":
		if request.form.get("CHANGE USERNAME"):
			print("HERE")
			error = check_new_user_name_db(user_id, request.form["password"], request.form["new_user_name"])

			if not error:
				user_name = request.form["new_user_name"]
				return redirect(url_for("message", msg = "User Name Updated"))

			return render_template("account.html", usr = user_name, usr_id = user_id, image = image, error = error)

		elif request.form.get("CHANGE PASSWORD"):
			error = check_new_password_db(user_id, request.form["password"], request.form["new_password"], request.form["re_new_password"])
			
			if not error:
				return redirect(url_for("message", msg = "Password Updated"))

			return render_template("account.html", usr = user_name, usr_id = user_id, image = image, error1 = error)
		
		elif request.form.get("DEL ACCOUNT"):
			error = check_password_delete_db(user_id, request.form["password"])

			if not error:
				user_id = None
				user_name = None
				return redirect(url_for("message", msg = "Account Deleted."))

			return render_template("account.html", usr = user_name, usr_id = user_id, image = image, error2 = error)


	return render_template("account.html", usr = user_name, usr_id = user_id, image = image)

# logout endpoint
@app.route("/logout")
def logout():
	global user_id, user_name
	user_id = None
	user_name = None
	return redirect(url_for("login"))


# login endpoint
@app.route("/login", methods = ["GET", "POST"])
def login():
	global user_id, user_name
	if user_id:
		return redirect(url_for("home"))

	error = None
	if request.method == "POST":
		# Login
		if check_user_db(request.form["username"], request.form["password"]):
			user_name = request.form["username"]
			user_id = get_user_id_db(user_name)
			return redirect(url_for("home"))
		else:
			error = "Invalid credentials. Please try again."

	return render_template("login.html", error = error, image = image)


# signup endopint
@app.route("/signup", methods = ["GET", "POST"])
def signup():
	global user_id, user_name
	if user_id:
		return redirect(url_for("home"))

	error = None
	if request.method == "POST":
		error = check_new_user_db(request.form["username"], request.form["password"], request.form["repassword"])

		# Sign Up
		if not error:
			user_name = request.form["username"]
			user_id = get_user_id_db(user_name)
			return redirect(url_for("home"))

	return render_template("signup.html", error = error, image = image)

# terms_and_privacy endopint
@app.route("/terms_and_privacy")
def terms_and_privacy():
	return render_template("terms_and_privacy.html", image = image)


# **************** MAIN ****************

if __name__ == "__main__":
	# connect to the PostgreSQL server
	connect_db(host="localhost", database=sys.argv[1], user="dbms_project", password="dbms_project")

	# Starting the server
	app.run(debug = True) # Debug mode will give us the bugger that we can use in a browser and auto-reload function

	# closing the server
	close_db()

