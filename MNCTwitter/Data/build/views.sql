CREATE VIEW company_tweet_stats(day, ticker_symbol, tweet_num, rank) AS
SELECT DATE(TO_TIMESTAMP(t.post_date)), ct.ticker_symbol, COUNT(*), rank() 
	OVER(PARTITION BY DATE(TO_TIMESTAMP(t.post_date)) ORDER BY COUNT(*) DESC)
FROM tweet t, company_tweet ct
WHERE ct.tweet_id = t.tweet_id
GROUP BY DATE(TO_TIMESTAMP(t.post_date)), ct.ticker_symbol;

CREATE MATERIALIZED VIEW streaks(ticker_symbol, start_date, end_date, length) AS
WITH RECURSIVE all_streaks(ticker_symbol, start_date, end_date, length) AS
(
	SELECT ticker_symbol, day, day, 1 FROM day_toppers

	UNION

	SELECT ast.ticker_symbol, start_date, day, length + 1
	FROM all_streaks ast, day_toppers dt
	WHERE
		dt.ticker_symbol = ast.ticker_symbol AND 
		day = end_date + '1 day'::interval
),
day_toppers AS (SELECT day, ticker_symbol FROM company_tweet_stats WHERE rank = 1)
SELECT ticker_symbol, start_date, end_date, length FROM
	(
		SELECT ticker_symbol, start_date, end_date, length, rank()
				OVER(PARTITION BY ticker_symbol ORDER BY length DESC, start_date DESC)
		FROM all_streaks
	) rankfilter
WHERE rank = 1;


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
SELECT * FROM
(
	SELECT tweet.tweet_id, writer_id, user_name, body, post_date, is_retweet, original_tweet_id, ph.hash, ph.tweet_num, ROW_NUMBER () OVER(PARTITION BY ph.hash ORDER BY ph.tweet_num DESC, post_date DESC)
	FROM tweet, users, tweet_hash th, popular_hashes ph
	WHERE
		writer_id = user_id AND
		tweet.tweet_id = th.tweet_id AND
		th.hash = ph.hash
) row_filter
WHERE row_number <= 100;
