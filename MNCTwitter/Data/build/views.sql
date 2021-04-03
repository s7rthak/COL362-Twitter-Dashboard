CREATE VIEW recommendations(u, recommendation, distance) AS
WITH RECURSIVE connects (u, rec_u, distance) AS 
(
	SELECT user_id2, user_id1, 1
	FROM follower f
	WHERE user_id1 <> user_id2

	UNION

	SELECT u, user_id1, distance + 1
	FROM connects, follower
	WHERE distance < 2 AND user_id2 = rec_u
	AND user_id1 <> u
)
SELECT u, rec_u, MIN(distance)
FROM connects
GROUP BY u, rec_u
HAVING MIN(distance) > 1;

CREATE VIEW company_tweet_stats(day, ticker_symbol, tweet_num, rank) AS
SELECT DATE(TO_TIMESTAMP(t.post_date)), ct.ticker_symbol, COUNT(*), rank() 
	OVER(PARTITION BY DATE(TO_TIMESTAMP(t.post_date)) ORDER BY COUNT(*) DESC)
FROM tweet t, company_tweet ct
WHERE ct.tweet_id = t.tweet_id
GROUP BY DATE(TO_TIMESTAMP(t.post_date)), ct.ticker_symbol; 

-- CREATE MATERIALIZED VIEW streaks(ticker_symbol, start_date, end_date, length) AS
-- WITH day_toppers AS (SELECT day, ticker_symbol FROM company_tweet_stats WHERE rank = 1),
-- RECURSIVE all_streaks(ticker_symbol, start_date, end_date, length) AS
-- (
-- 	SELECT ticker_symbol, day, day, 1 FROM day_toppers

-- 	UNION

-- 	SELECT ticker_symbol, start_date, day, length + 1, rank()
-- 		OVER(PARTITION BY ticker_symbol ORDER BY length DESC, start_date DESC)
-- 	FROM all_streaks ast, day_toppers dt
-- 	WHERE
-- 		dt.ticker_symbol = all_streaks.ticker_symbol AND 
-- 		day = end_date + '1 day'::interval
-- )
-- SELECT ticker_symbol, start_date, end_date, length
-- FROM all_streaks
-- GROUP BY ticker_symbol

-- SELECT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, ph.hash, ph.tweet_num
-- FROM tweet, users, tweet_hash th, popular_hashes ph
-- WHERE
-- 	writer_id = user_id AND
-- 	tweet.tweet_id = th.tweet_id AND
-- 	th.hash = ph.hash
-- ORDER BY ph.tweet_num DESC, ph.hash ASC, post_date DESC
-- LIMIT 100;


CREATE MATERIALIZED VIEW popular_users(user_id, user_name) AS
SELECT user_id, user_name
FROM users
ORDER BY ((like_num + comment_num - report_num) * (1 + retweet_num) * follower_num) DESC
LIMIT 500;

CREATE MATERIALIZED VIEW popular_tweets(tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id) AS
SELECT tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id
FROM tweet, users
WHERE writer_id = user_id
ORDER BY ((tweet.like_num + tweet.comment_num - tweet.report_num) * (1 + tweet.retweet_num)) DESC
LIMIT 500;

CREATE MATERIALIZED VIEW popular_hashes_tweets(tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, hash, tweet_num) AS
WITH popular_hashes AS
(
	SELECT th1.hash, COUNT(*) AS tweet_num
	FROM tweet_hash th1
	GROUP BY hash
	ORDER BY COUNT(*) DESC
	LIMIT 20
)
SELECT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, ph.hash, ph.tweet_num
FROM tweet, users, tweet_hash th, popular_hashes ph
WHERE
	writer_id = user_id AND
	tweet.tweet_id = th.tweet_id AND
	th.hash = ph.hash
ORDER BY ph.tweet_num DESC, ph.hash ASC, post_date DESC
LIMIT 100;