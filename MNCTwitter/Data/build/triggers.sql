-- *********************** TRIGGERS ***********************
-- Verify:
-- 	Inc -> Dec (3 places)
-- 	user should be writer of the tweet inserted/deleted
-- 	new -> old (condition and return)
-- 	After delete

-- Actions and triggers in tweet --

-- trigger on users(tweet_num) --
	-- INSERT tweet
	CREATE OR REPLACE FUNCTION inc_tweet_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET tweet_num = users.tweet_num + 1
		WHERE new.writer_id = users.user_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementTweetNum
	AFTER INSERT ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE inc_tweet_num();

	-- DELETE Tweet
	CREATE OR REPLACE FUNCTION dec_tweet_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET tweet_num = users.tweet_num - 1
		WHERE old.writer_id = users.user_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementTweetNum
	AFTER DELETE ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE dec_tweet_num();

-- trigger on tweet(retweet_num) --
	-- INSERT retweet
	CREATE OR REPLACE FUNCTION inc_retweet_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET retweet_num = tweet.retweet_num + 1
		WHERE new.original_tweet_id = tweet.tweet_id AND new.is_retweet;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementRetweetNum
	BEFORE INSERT ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE inc_retweet_num();

	-- DELETE retweet
	CREATE OR REPLACE FUNCTION dec_retweet_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET retweet_num = tweet.retweet_num - 1
		WHERE old.original_tweet_id = tweet.tweet_id AND old.is_retweet;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementRetweetNum
	AFTER DELETE ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE dec_retweet_num();

-- trigger on users(retweet_num) --
	-- INSERT retweet
	CREATE OR REPLACE FUNCTION inc_retweet_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET retweet_num = users.retweet_num + 1
		FROM tweet tweet1
		WHERE new.original_tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id AND new.is_retweet;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementRetweetNum1
	AFTER INSERT ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE inc_retweet_num1();

	-- DELETE retweet
	CREATE OR REPLACE FUNCTION dec_retweet_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET retweet_num = users.retweet_num - 1
		FROM tweet tweet1
		WHERE old.original_tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id AND old.is_retweet;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementRetweetNum1
	AFTER DELETE ON tweet
	FOR EACH ROW
		EXECUTE PROCEDURE dec_retweet_num1();

-- INSERT into tweet_hash --
-- UPDATE tweet_hash --


-- Actions and triggers in follower --

-- trigger on users(tweet_id, follower_num) --
	-- INSERT follower
	CREATE OR REPLACE FUNCTION inc_foll_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET follower_num = users.follower_num + 1
		WHERE new.user_id1 = users.user_id;
		
		UPDATE users
		SET follow_num = follow_num + 1
		WHERE new.user_id2 = users.user_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementFollNum
	AFTER INSERT ON follower
	FOR EACH ROW
		EXECUTE PROCEDURE inc_foll_num();

	-- DELETE follower
	CREATE OR REPLACE FUNCTION dec_foll_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET follower_num = users.follower_num - 1
		WHERE old.user_id1 = users.user_id;

		UPDATE users
		SET follow_num = follow_num - 1
		WHERE old.user_id2 = users.user_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementFollNum
	AFTER DELETE ON follower
	FOR EACH ROW
		EXECUTE PROCEDURE dec_foll_num();

-- Actions and triggers in favourite --

-- trigger on tweet(like_num) --
	-- INSERT like
	CREATE OR REPLACE FUNCTION inc_like_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET like_num = tweet.like_num + 1
		WHERE new.tweet_id = tweet.tweet_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementLikeNum
	AFTER INSERT ON favourite
	FOR EACH ROW
		EXECUTE PROCEDURE inc_like_num();

	-- DELETE like
	CREATE OR REPLACE FUNCTION dec_like_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET like_num = tweet.like_num - 1
		WHERE old.tweet_id = tweet.tweet_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementLikeNum
	AFTER DELETE ON favourite
	FOR EACH ROW
		EXECUTE PROCEDURE dec_like_num();

-- trigger on users(like_num) --
	-- INSERT like
	CREATE OR REPLACE FUNCTION inc_like_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET like_num = users.like_num + 1
		FROM tweet tweet1
		WHERE new.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementLikeNum1
	AFTER INSERT ON favourite
	FOR EACH ROW
		EXECUTE PROCEDURE inc_like_num1();

	-- DELETE like
	CREATE OR REPLACE FUNCTION dec_like_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET like_num = users.like_num - 1
		FROM tweet tweet1
		WHERE old.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementLikeNum1
	AFTER DELETE ON favourite
	FOR EACH ROW
		EXECUTE PROCEDURE dec_like_num1();

-- Actions and triggers in comment --

-- trigger on tweet(comment_num) --
	-- INSERT comment
	CREATE OR REPLACE FUNCTION inc_comment_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET comment_num = tweet.comment_num + 1
		WHERE new.tweet_id = tweet.tweet_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementCommentNum
	AFTER INSERT ON comment
	FOR EACH ROW
		EXECUTE PROCEDURE inc_comment_num();

	-- DELETE comment
	CREATE OR REPLACE FUNCTION dec_comment_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET comment_num = tweet.comment_num - 1
		WHERE old.tweet_id = tweet.tweet_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementCommentNum
	AFTER DELETE ON comment
	FOR EACH ROW
		EXECUTE PROCEDURE dec_comment_num();

-- trigger on users(comment_num) --
	-- INSERT comment
	CREATE OR REPLACE FUNCTION inc_comment_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET comment_num = users.comment_num + 1
		FROM tweet tweet1
		WHERE new.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementCommentNum1
	AFTER INSERT ON comment
	FOR EACH ROW
		EXECUTE PROCEDURE inc_comment_num1();

	-- DELETE comment
	CREATE OR REPLACE FUNCTION dec_comment_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET comment_num = users.comment_num - 1
		FROM tweet tweet1
		WHERE old.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementCommentNum1
	AFTER DELETE ON comment
	FOR EACH ROW
		EXECUTE PROCEDURE dec_comment_num1();

-- Actions and triggers in report --

-- trigger on tweet(report_num) --
	-- INSERT report
	CREATE OR REPLACE FUNCTION inc_report_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET report_num = tweet.report_num + 1
		WHERE new.tweet_id = tweet.tweet_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementReportNum
	AFTER INSERT ON report
	FOR EACH ROW
		EXECUTE PROCEDURE inc_report_num();

	-- DELETE report
	CREATE OR REPLACE FUNCTION dec_report_num() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE tweet
		SET report_num = tweet.report_num - 1
		WHERE old.tweet_id = tweet.tweet_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementReportNum
	AFTER DELETE ON report
	FOR EACH ROW
		EXECUTE PROCEDURE dec_report_num();

-- trigger on users(report_num) --
	-- INSERT report
	CREATE OR REPLACE FUNCTION inc_report_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET report_num = users.report_num + 1
		FROM tweet tweet1
		WHERE new.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN new;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER IncrementReportNum1
	AFTER INSERT ON report
	FOR EACH ROW
		EXECUTE PROCEDURE inc_report_num1();

	-- DELETE report
	CREATE OR REPLACE FUNCTION dec_report_num1() RETURNS TRIGGER AS
	$BODY$
	BEGIN
		UPDATE users
		SET report_num = users.report_num - 1
		FROM tweet tweet1
		WHERE old.tweet_id = tweet1.tweet_id AND tweet1.writer_id = users.user_id;

		RETURN old;
	END;
	$BODY$
	language plpgsql;

	CREATE TRIGGER DecrementReportNum1
	AFTER DELETE ON report
	FOR EACH ROW
		EXECUTE PROCEDURE dec_report_num1();
