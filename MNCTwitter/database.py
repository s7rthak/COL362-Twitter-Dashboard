import psycopg2
from query import *
import time
from datetime import datetime
import re
from timing import *

# **************** MANAGING DATABASE CONNECTIONS ****************

conn = None # Connection to PostgreSQL server
cur = None # Communication cursor to PostgreSQL

def extract(ind):
	def extract_index(tup):
		return tup[ind]
	return extract_index

def convert_timestamp(ind):
	def convert_timestamp_index(tup):
		new_tup = []
		for i in range(len(tup)):
			if i == ind:
				new_tup.append(datetime.fromtimestamp(tup[i]))
			else:
				new_tup.append(tup[i])
		return tuple(new_tup)
	return convert_timestamp_index

def connect_db(host, database, user, password):
	""" Connect to the PostgreSQL database server """
	print("Connecting to the PostgreSQL database...")

	try:
		global conn, cur

		# connect to the PostgreSQL server
		conn = psycopg2.connect(host=host, database=database, user=user, password=password)

		# for logging time
		conn = psycopg2.connect(connection_factory=MyLoggingConnection, host=host, database=database, user=user, password=password)
		conn.initialize(logger)

		# create a cursor
		cur = conn.cursor()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def close_db():
	""" Closes connection to Database """
	# close the communication with the PostgreSQL
	if cur is not None:
		cur.close()
		print("Communication cursor with PostgreSQL closed.")

	# closing the connection to PostgreSQL
	if conn is not None:
		conn.close()
		print("Database connection closed.")


def check_user_db(user_name, password):
	""" Returns boolean if user_name, password is valid for a current user """
	cur.execute(check_user_query, (user_name, password))
	return cur.fetchone()[0]

def check_new_user_db(user_name, password, repassword):
	""" Returns error message if any on given inputs for new user """
	cur.execute(check_new_user_query, (user_name,))
	if not cur.fetchone()[0]:
		return "That user_name is taken. Try another."
	if password != repassword:
		return "Those passwords didn't match. Try again."
	cur.execute(insert_new_user_query, (user_name, password))
	conn.commit()

# Write tweet_hash.csv
def extract_hashtags_db(text):
    rep = {"'": " ", "#": " #", "http": " http", ",": "", '"': ''}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    all_hashtags = list(set([re.sub(r"#+", "#", k) for k in set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in text.split() if i.startswith("#")])])]))
    all_hashtags = [hashtag[1:] for hashtag in all_hashtags]
    return all_hashtags

def post_tweet_db(user_id, body, company_tickers, original_tweet = None):
	""" Inserts new tweet to the tweet table """
	# Updating tweet
	cur.execute(insert_new_tweet_query, (user_id, int(time.time()), body, original_tweet != None, original_tweet))
	new_tweet_id = cur.fetchone()[0]

	# Updating company_tweet
	for company in company_tickers:
		cur.execute(insert_new_tweet_company_query, (new_tweet_id, company))

	# Updating tweet_hash
	for hashtag in extract_hashtags_db(body):
		cur.execute(insert_new_tweet_hash_query, (new_tweet_id, hashtag))

	conn.commit()

def get_popular_users_db():
	""" Returns popular users """
	cur.execute(get_popular_users_query)
	return list(map(extract(0), cur.fetchall()))

def get_popular_tweets_db():
	""" Returns popular tweets """
	cur.execute(get_popular_tweets_query)
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_users_followed_by_db(user_id):
	""" Returns users followed by user """
	cur.execute(get_users_followed_by_query, (user_id,))
	return list(map(extract(0), cur.fetchall()))

def get_followers_db(user_id):
	""" Returns user's followers of user """
	cur.execute(get_followers_query, (user_id,))
	return list(map(extract(0), cur.fetchall()))

def get_user_id_db(user_name):
	""" returns user_id of user_name (if invalid returns None) """
	cur.execute(get_user_id_query, (user_name,))
	user_id = cur.fetchone()
	if user_id:
		return user_id[0]

def get_user_name_db(user_id):
	""" Returns the user_name of user_id """
	cur.execute(get_user_name_query, (user_id,))
	return cur.fetchone()[0]

def get_company_name_db(company_ticker):
	""" Returns company name given company ticker """
	cur.execute(get_company_name_query, (company_ticker,))
	return cur.fetchone()[0]

def get_all_user_hash_tweets_db(company_tickers, hashes, time_range, order_by):
	""" List of hash_tweets with given constriants """
	after_time = int(time.time()) - time_range
	cur.execute(get_all_user_hash_tweets_query + order_by + " DESC LIMIT 100", (company_tickers, hashes, after_time))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_all_user_tweets_db(company_tickers, time_range, order_by):
	""" List of tweets with given constriants """
	after_time = int(time.time()) - time_range
	cur.execute(get_all_user_tweets_query + order_by + " DESC LIMIT 100", (company_tickers, after_time))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_hash_tweets_db(user_ids, company_tickers, hashes, time_range, order_by):
	""" List of hash_tweets with given constriants """
	after_time = int(time.time()) - time_range
	cur.execute(get_hash_tweets_query + order_by + " DESC LIMIT 100", (user_ids, company_tickers, hashes, after_time))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_tweets_db(user_ids, company_tickers, time_range, order_by):
	""" List of tweets with given constriants """
	after_time = int(time.time()) - time_range
	cur.execute(get_tweets_query + order_by + " DESC LIMIT 100", (user_ids, company_tickers, after_time))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_tweet_db(tweet_id):
	""" Returns tweet given tweet_id """
	# tweet_info = 0: tweet_id, 1: writer_id, 2: user_name, 3: body, 4: post_date, 5: tweet.comment_num, 6: tweet.retweet_num, 7: tweet.like_num, 8: tweet.report_num, 9: is_retweet, 10: original_tweet_id
	cur.execute(get_tweet_query, (tweet_id,))
	return list(map(convert_timestamp(4), cur.fetchall()))[0]

def add_like_db(user_id, tweet_id):
	""" Add like """
	cur.execute(add_like_query, (user_id, tweet_id))
	conn.commit()

def delete_like_db(user_id, tweet_id):
	""" Removes like """
	cur.execute(delete_like_query, (user_id, tweet_id))
	conn.commit()

def get_companies_db(tweet_id):
	""" Returns companies of tweet_id """
	cur.execute(get_companies_query, (tweet_id,))
	return list(map(extract(0), cur.fetchall()))

def add_retweet_db(user_id, tweet_id):
	""" Retweet this tweet """
	tweet_info = get_tweet_db(tweet_id)
	company_tickers = get_companies_db(tweet_id)
	post_tweet_db(user_id, tweet_info[3], company_tickers, tweet_id)

def find_retweet_db(user_id, tweet_id):
	""" Finds the retweeted tweet tweeted by user_id """
	cur.execute(find_retweet_query, (user_id, tweet_id))
	return cur.fetchone()[0]

def delete_retweet_db(user_id, tweet_id):
	""" Deletes retweet """
	retweet_id = find_retweet_db(user_id,tweet_id)
	delete_tweet_db(retweet_id)

def add_report_db(user_id, tweet_id):
	""" Add report """
	cur.execute(add_report_query, (user_id, tweet_id))
	conn.commit()

def delete_report_db(user_id, tweet_id):
	""" Removes report """
	cur.execute(delete_report_query, (user_id, tweet_id))
	conn.commit()

def delete_tweet_db(tweet_id):
	""" Delete this tweet """
	cur.execute(delete_tweet_query, (tweet_id,))
	conn.commit()

def add_comment_db(user_id, tweet_id, body):
	""" Add new comment """
	cur.execute(add_comment_query, (user_id, tweet_id, int(time.time()), body))
	conn.commit()

def check_like_db(user_id, tweet_id):
	""" Does user_id like tweet_id """
	cur.execute(check_like_query, (user_id, tweet_id))
	return cur.fetchone()[0]

def check_retweet_db(user_id, tweet_id):
	""" Has user_id retweeted tweet_id """
	cur.execute(check_retweet_query, (user_id, tweet_id))
	return cur.fetchone()[0]

def check_report_db(user_id, tweet_id):
	""" Has user_id reported tweet_id """
	cur.execute(check_report_query, (user_id, tweet_id))
	return cur.fetchone()[0]

def get_comment_list_db(user_id, tweet_id):
	""" Comments on tweet_id and their ownership wrt user_id """
	# comment_info: comment_id, user_id, user_name, tweet_id, comment_date, body
	cur.execute(get_comment_list_query, (tweet_id,))
	comments = cur.fetchall()
	return [[convert_timestamp(4)(comment), comment[1] == user_id] for comment in comments]

def delete_comment_db(comment_id):
	""" Delete comment_id """
	cur.execute(delete_comment_query, (comment_id,))
	conn.commit()

def get_all_user_ids_db():
	""" Returns all valid user_ids """
	cur.execute(get_all_user_ids_query)
	return map(extract(0), cur.fetchall())

def get_user_info_db(user_id):
	""" Information of this user """
	cur.execute(get_user_info_query, (user_id,))
	return cur.fetchone()

def get_user_tweets_db(user_id):
	""" All tweets of this user """
	cur.execute(get_user_tweets_query, (user_id,))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_is_popular_db(user_id):
	""" Is this user popular """
	cur.execute(get_is_popular_query, (user_id,))
	return cur.fetchone()[0]

def get_users_followed_by_limit_db(user_id, limit):
	""" Returns limited users followed by user """
	cur.execute(get_users_followed_by_limit_query, (user_id, limit))
	return cur.fetchall()

def get_followers_limit_db(user_id, limit):
	""" Returns limited user's followers of user """
	cur.execute(get_followers_limit_query, (user_id, limit))
	return cur.fetchall()

def delete_follow_db(user_id_page, user_id):
	"""  user_id unfollows user_id_page """
	cur.execute(delete_follow_query, (user_id_page, user_id))
	conn.commit()

def add_follow_db(user_id_page, user_id):
	"""  user_id follows user_id_page """
	cur.execute(add_follow_query, (user_id_page, user_id))
	conn.commit()

def get_common_follow_list_db(user_id, user_id_page):
	""" returns limited number of common follows """
	cur.execute(get_common_follow_list_query, (user_id, user_id_page))
	return cur.fetchall()

def get_common_follower_list_db(user_id, user_id_page):
	""" returns limited number of common followers """
	cur.execute(get_common_follower_list_query, (user_id, user_id_page))
	return cur.fetchall()

def check_new_user_name_db(user_id, password, new_user_name):
	""" Checks password, updates username if correct password and unique username """
	if not check_password_db(user_id, password):
		return "Wrong password."

	cur.execute(check_new_user_query, (new_user_name,))
	if not cur.fetchone()[0]:
		return "That user_name is taken. Try another."

	cur.execute(update_user_name_query, (new_user_name, user_id))
	conn.commit()

def check_new_password_db(user_id, password, new_password, re_new_password):
	""" checks password, updates password if matches with rewrite """
	if not check_password_db(user_id, password):
		return "Wrong password."

	if new_password != re_new_password:
		return "Those passwords didn't match. Try again."

	cur.execute(update_password_query, (new_password, user_id))
	conn.commit()

def check_password_db(user_id, password):
	""" checks password """
	cur.execute(password_match_query, (user_id, password))
	return cur.fetchone()[0]

def check_password_delete_db(user_id, password):
	""" checks password, deletes account """
	if not check_password_db(user_id, password):
		return "Wrong password."

	cur.execute(delete_user_query, (user_id,))
	conn.commit()

def get_observers_db(user_id):
	""" Returns user's observers for network analysis """
	cur.execute(get_observers_query, (user_id, user_id, user_id, user_id))
	return list(map(extract(0), cur.fetchall()))

def get_matching_db(user_id):
	""" Returns users with whom user_id's interests match """
	cur.execute(get_matching_query, (user_id, user_id, user_id))
	return list(map(extract(0), cur.fetchall()))

def get_recommendations_db(user_id):
	""" Returns user's close users for network analysis """
	cur.execute(get_recommendations_query, (user_id, user_id))
	return list(map(extract(0), cur.fetchall()))

def get_topfans_db(company_id):
	cur.execute(get_topfans_query, (company_id, ))
	return list(map(extract(0), cur.fetchall()))

def get_totallikes_db(company_id):
	cur.execute(get_totallikes_query, (company_id, ))
	return cur.fetchone()[0]

def get_mosttrending_db(company_id):
	cur.execute(get_mosttrending_query, (company_id, ))
	return cur.fetchone()[0]

def get_longest_streak_db(company_id):
	cur.execute(get_longest_streak_query, (company_id, ))
	return cur.fetchone()

def get_maxtweets_db(company_id):
	cur.execute(get_maxtweets_query, (company_id, ))
	return list(cur.fetchall())

def get_hash_tweets_db(hashtag):
	""" Returns all tweets of given hashtag fast """
	cur.execute(get_hash_tweets_query, (hashtag,))
	return list(map(convert_timestamp(4), cur.fetchall()))

def get_popular_hashes_db():
	""" returns popular hashtags fast """
	cur.execute(get_popular_hashes_query)
	return list(map(extract(0), cur.fetchall()))

def check_db():
	
	cur.execute("SELECT * FROM tweet;")
	l = cur.fetchall()
	print("**** tweet ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM company_tweet;")
	l = cur.fetchall()
	print("**** company_tweet ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM company;")
	l = cur.fetchall()
	print("**** company ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM users;")
	l = cur.fetchall()
	print("**** users ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM follower;")
	l = cur.fetchall()
	print("**** follower ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM favourite;")
	l = cur.fetchall()
	print("**** favourite ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM comment;")
	l = cur.fetchall()
	print("**** comment ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM report;")
	l = cur.fetchall()
	print("**** report ****")
	for i in l:
		print(i)
		
	cur.execute("SELECT * FROM tweet_hash;")
	l = cur.fetchall()
	print("**** tweet_hash ****")
	for i in l:
		print(i)
