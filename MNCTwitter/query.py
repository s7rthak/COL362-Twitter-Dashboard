# **************** QUERIES ****************
check_user_query = "SELECT COUNT(*) = 1 FROM users WHERE user_name = %s AND password = %s;"

check_new_user_query = "SELECT COUNT(*) = 0 FROM users WHERE user_name = %s;"

insert_new_user_query = "INSERT INTO users(user_id, user_name, password, tweet_num, follower_num, follow_num, comment_num, retweet_num, like_num, report_num) VALUES(DEFAULT, %s, %s, 0, 0, 0, 0, 0, 0, 0)"

insert_new_tweet_query = "INSERT INTO tweet(tweet_id, writer_id, post_date, body, comment_num, retweet_num, like_num, report_num, is_retweet, original_tweet_id) VALUES(DEFAULT, %s, %s, %s, 0, 0, 0, 0, %s, %s) RETURNING tweet_id"

insert_new_tweet_company_query = "INSERT INTO company_tweet(tweet_id, ticker_symbol) VALUES(%s, %s)"

insert_new_tweet_hash_query = "INSERT INTO tweet_hash(tweet_id, hash) VALUES(%s, %s)"

get_popular_users_query = "SELECT user_id FROM popular_users"

get_popular_tweets_query = "SELECT * FROM popular_tweets"

get_users_followed_by_query = "SELECT user_id1 FROM follower WHERE user_id2 = %s"

get_followers_query = "SELECT user_id2 FROM follower WHERE user_id1 = %s"

get_user_id_query = "SELECT user_id FROM users WHERE user_name = %s"

get_user_name_query = "SELECT user_name FROM users WHERE user_id = %s"

get_company_name_query = "SELECT company_name FROM company WHERE ticker_symbol = %s"

get_all_user_hash_tweets_query = \
"SELECT DISTINCT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, tweet.like_num, tweet.retweet_num, tweet.report_num, tweet.comment_num \
FROM tweet, users, company_tweet \
WHERE \
	writer_id = user_id AND \
	tweet.tweet_id = company_tweet.tweet_id AND \
	 \
	ticker_symbol = ANY(%s) AND \
	(SELECT COUNT(*) FROM ((SELECT hash FROM tweet_hash WHERE tweet.tweet_id = tweet_hash.tweet_id) INTERSECT (SELECT * FROM unnest(%s))) common_hashes) > 0 AND \
	post_date >= %s \
	ORDER BY tweet."

get_all_user_tweets_query = \
"SELECT DISTINCT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, tweet.like_num, tweet.retweet_num, tweet.report_num, tweet.comment_num \
FROM tweet, users, company_tweet \
WHERE \
	writer_id = user_id AND \
	tweet.tweet_id = company_tweet.tweet_id AND \
	 \
	ticker_symbol = ANY(%s) AND \
	post_date >= %s \
	ORDER BY tweet."

get_hash_tweets_query = \
"SELECT DISTINCT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, tweet.like_num, tweet.retweet_num, tweet.report_num, tweet.comment_num \
FROM tweet, users, company_tweet \
WHERE \
	writer_id = user_id AND \
	tweet.tweet_id = company_tweet.tweet_id AND \
	 \
	writer_id = ANY(%s) AND \
	ticker_symbol = ANY(%s) AND \
	(SELECT COUNT(*) FROM ((SELECT hash FROM tweet_hash WHERE tweet.tweet_id = tweet_hash.tweet_id) INTERSECT (SELECT * FROM unnest(%s))) common_hashes) > 0 AND \
	post_date >= %s \
	ORDER BY tweet."

get_tweets_query = \
"SELECT DISTINCT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, tweet.like_num, tweet.retweet_num, tweet.report_num, tweet.comment_num \
FROM tweet, users, company_tweet \
WHERE \
	writer_id = user_id AND \
	tweet.tweet_id = company_tweet.tweet_id AND \
	 \
	writer_id = ANY(%s) AND \
	ticker_symbol = ANY(%s) AND \
	post_date >= %s \
	ORDER BY tweet."

get_tweet_query = \
"SELECT tweet_id, writer_id, user_name, body, post_date, tweet.comment_num, tweet.retweet_num, tweet.like_num, tweet.report_num, is_retweet, original_tweet_id \
FROM tweet, users \
WHERE \
	writer_id = user_id AND \
	 \
	tweet_id = %s"

add_like_query = "INSERT INTO favourite(user_id, tweet_id) VALUES(%s, %s)"

delete_like_query = "DELETE FROM favourite WHERE user_id = %s AND tweet_id = %s"

find_retweet_query = "SELECT tweet_id FROM tweet WHERE is_retweet AND writer_id = %s AND original_tweet_id = %s"

add_report_query = "INSERT INTO report(user_id, tweet_id) VALUES(%s, %s)"

delete_report_query = "DELETE FROM report WHERE user_id = %s AND tweet_id = %s"

delete_tweet_query = "DELETE FROM tweet WHERE tweet_id = %s"

add_comment_query = "INSERT INTO comment(comment_id, user_id, tweet_id, comment_date, body) VALUES(DEFAULT, %s, %s, %s, %s)"

check_like_query = "SELECT COUNT(*) > 0 FROM favourite WHERE user_id = %s AND tweet_id = %s"

check_retweet_query = "SELECT COUNT(*) > 0 FROM tweet WHERE writer_id = %s AND is_retweet AND original_tweet_id = %s"

check_report_query = "SELECT COUNT(*) > 0 FROM report WHERE user_id = %s AND tweet_id = %s"

get_comment_list_query = "SELECT comment_id, comment.user_id, user_name, tweet_id, comment_date, body FROM comment, users WHERE comment.user_id = users.user_id AND tweet_id = %s ORDER BY comment_date"

delete_comment_query = "DELETE FROM comment WHERE comment_id = %s"

get_companies_query = "SELECT DISTINCT ticker_symbol FROM company_tweet WHERE tweet_id = %s"

get_all_user_ids_query = "SELECT user_id FROM users LIMIT 1000"

get_user_info_query = "SELECT * FROM users WHERE user_id = %s"

get_user_tweets_query = "SELECT DISTINCT tweet.tweet_id, writer_id, 0, body, post_date, is_retweet, original_tweet_id FROM tweet WHERE writer_id = %s"

get_is_popular_query = \
"SELECT COUNT(*) > 0 \
FROM \
popular_users \
WHERE user_id = %s"

get_users_followed_by_limit_query = "SELECT user_id1, user_name FROM follower, users WHERE user_id1 = user_id AND user_id2 = %s LIMIT %s"

get_followers_limit_query = "SELECT user_id2, user_name FROM follower, users WHERE user_id2 = user_id AND user_id1 = %s LIMIT %s"

delete_follow_query = "DELETE FROM follower WHERE user_id1 = %s AND user_id2 = %s"

add_follow_query = "INSERT INTO follower(user_id1, user_id2) VALUES(%s, %s)"

get_common_follow_list_query = \
"SELECT user_id1, user_name FROM follower, users WHERE user_id1 = user_id AND user_id2 = %s \
	INTERSECT \
SELECT user_id1, user_name FROM follower, users WHERE user_id1 = user_id AND user_id2 = %s"

get_common_follower_list_query = \
"SELECT user_id2, user_name FROM follower, users WHERE user_id2 = user_id AND user_id1 = %s \
	INTERSECT \
SELECT user_id2, user_name FROM follower, users WHERE user_id2 = user_id AND user_id1 = %s"

update_user_name_query = "UPDATE users SET user_name = %s WHERE user_id = %s"

update_password_query = "UPDATE users SET password = %s WHERE user_id = %s"

password_match_query = "SELECT COUNT(*) > 0 FROM users WHERE user_id = %s and password = %s"

delete_user_query = "DELETE FROM users WHERE user_id = %s"

get_observers_query = \
"SELECT user_id2 FROM follower WHERE user_id1 = %s UNION \
SELECT f.user_id FROM tweet t, favourite f WHERE t.tweet_id = f.tweet_id AND t.writer_id = %s UNION \
SELECT c.user_id FROM tweet t, comment c WHERE t.tweet_id = c.tweet_id AND t.writer_id = %s UNION \
SELECT r.user_id FROM tweet t, report r WHERE t.tweet_id = r.tweet_id AND t.writer_id = %s"

get_matching_query = \
"WITH RECURSIVE connects(recommendation, distance) AS  \
( \
	SELECT user_id1, 1 \
	FROM follower \
	WHERE user_id2 = %s \
 \
	UNION \
 \
	SELECT user_id1, distance + 1 \
	FROM connects, follower \
	WHERE distance < 4 AND user_id2 = recommendation \
	AND user_id1 <> %s \
), \
our_user_follows AS (SELECT user_id1 FROM follower WHERE user_id2 = %s), \
our_user_follow_num AS (SELECT CAST(COUNT(*) AS FLOAT) FROM our_user_follows) \
SELECT DISTINCT recommendation, \
	(SELECT COUNT(*) FROM follower WHERE user_id2 = recommendation AND user_id1 IN (SELECT * FROM our_user_follows)) / (SELECT * FROM our_user_follow_num) AS match \
FROM connects \
WHERE (SELECT COUNT(*) FROM follower WHERE user_id2 = recommendation AND user_id1 IN (SELECT * FROM our_user_follows)) / (SELECT * FROM our_user_follow_num) > 0 \
ORDER BY (SELECT COUNT(*) FROM follower WHERE user_id2 = recommendation AND user_id1 IN (SELECT * FROM our_user_follows)) / (SELECT * FROM our_user_follow_num) \
LIMIT 10"

get_recommendations_query = \
"WITH RECURSIVE connects(recommendation, distance) AS  \
( \
	SELECT user_id1, 1 \
	FROM follower \
	WHERE user_id2 = %s \
 \
	UNION \
 \
	SELECT user_id1, distance + 1 \
	FROM connects, follower \
	WHERE distance < 3 AND user_id2 = recommendation \
	AND user_id1 <> %s \
) \
SELECT DISTINCT recommendation from connects GROUP BY recommendation HAVING MIN(distance) > 1"

get_topfans_query = \
"SELECT t.writer_id \
FROM company_tweet ct, tweet t \
WHERE t.tweet_id = ct.tweet_id \
AND ct.ticker_symbol = %s \
GROUP BY t.writer_id \
ORDER BY COUNT(*) DESC \
LIMIT 10"

get_totallikes_query = \
"SELECT SUM(t.like_num) \
FROM company_tweet ct, tweet t \
WHERE ct.tweet_id=t.tweet_id AND ct.ticker_symbol=%s \
GROUP BY ct.ticker_symbol"

get_maxtweets_query = \
"SELECT day, tweet_num FROM \
( \
	SELECT day, tweet_num, rank() OVER(PARTITION BY ticker_symbol ORDER BY tweet_num DESC) \
	FROM company_tweet_stats \
	WHERE ticker_symbol = %s \
) rankfilter \
WHERE rank = 1"

get_mosttrending_query = \
"SELECT COUNT(*) FROM \
company_tweet_stats \
WHERE rank = 1 AND ticker_symbol = %s"

get_longest_streak_query = \
"SELECT start_date, end_date, length \
FROM streaks \
WHERE ticker_symbol = %s"

get_popular_hash_tweets_query = "SELECT * FROM popular_hashes_tweets WHERE hash = %s"

get_popular_hashes_query = "SELECT hash FROM popular_hashes_tweets GROUP BY hash, tweet_num ORDER BY tweet_num"
