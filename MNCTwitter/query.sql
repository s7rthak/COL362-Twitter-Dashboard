-- Actions and triggers in tweet --

-- trigger on users(tweet_num) --
CREATE OR REPLACE FUNCTION inc_tweet_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET tweet_num = tweet_num + 1 WHERE new.writer_id = users.user_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementTweetNum 
AFTER INSERT ON tweet
FOR EACH ROW 
    EXECUTE PROCEDURE inc_tweet_num();

-- INSERT into company_tweet --


-- trigger on tweet(retweet_num) -- 
CREATE OR REPLACE FUNCTION inc_retweet_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE tweet SET retweet_num = retweet_num + 1 WHERE new.original_tweet_id = tweet.tweet_id AND new.is_retweet;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementRetweetNum
BEFORE INSERT ON tweet
FOR EACH ROW
    EXECUTE PROCEDURE inc_retweet_num();

-- trigger on user(retweet_num) --
CREATE OR REPLACE FUNCTION inc_retweet_num1() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET retweet_num = retweet_num + 1 WHERE new.writer_id = users.user_id AND new.is_retweet;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementRetweetNum1
AFTER INSERT ON tweet
FOR EACH ROW
    EXECUTE PROCEDURE inc_retweet_num1();

-- INSERT into tweet_hash --

-- trigger on user(tweet_num) --
UPDATE users SET `tweet_num` = `tweet_num` - 1 WHERE users.writer = deleted.tweet_id;

-- DELETE retweeted tweets --
DELETE FROM tweet WHERE tweet_id IN (SELECT original_tweet_id FROM deleted.original_tweet_id);

-- UPDATE tweet_hash --


-- Actions and triggers in users --

-- DELETE tweet of the user --
DELETE FROM tweet WHERE deleted.user_name = tweet.writer;

-- DELETE from follower table --
DELETE FROM follower WHERE follower.user_id1 = deleted.user_id OR follower.user_id2 = deleted.user_id

-- Actions and triggers in follower -- 

-- trigger on user(tweet_id, follower_num) --
CREATE OR REPLACE FUNCTION inc_foll_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET follower_num = follower_num + 1 WHERE new.user_id1 = users.user_id;
    UPDATE users SET follow_num = follow_num + 1 WHERE new.user_id2 = users.user_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementFollNum
AFTER INSERT ON follower
FOR EACH ROW
    EXECUTE PROCEDURE inc_foll_num();

-- action on user(tweet_id, follower_num) -- 
UPDATE users SET `follower_num` = `follower_num` - 1 WHERE deleted.user_id1 = users.user_id

-- Actions and triggers in favourite --

-- trigger on users(like_num) --
CREATE OR REPLACE FUNCTION inc_like_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET like_num = like_num + 1 WHERE new.user_id = users.user_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementLikeNum
AFTER INSERT ON favourite
FOR EACH ROW
    EXECUTE PROCEDURE inc_like_num();

-- trigger on tweet(like_num) --
CREATE OR REPLACE FUNCTION inc_like_num1() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE tweet SET like_num = like_num + 1 WHERE new.tweet_id = tweet.tweet_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementLikeNum1
AFTER INSERT ON favourite
FOR EACH ROW
    EXECUTE PROCEDURE inc_like_num1();

-- delete tweet(like_num) --
UPDATE tweet SET `like_num` = `like_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `like_num` = `like_num` - 1 WHERE deleted.user_id = users.user_id;

-- Actions and triggers in comment --

-- trigger on users(comment_num) --
CREATE OR REPLACE FUNCTION inc_comment_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE tweet SET comment_num = comment_num + 1 WHERE new.tweet_id = tweet.tweet_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementCommentNum
AFTER INSERT ON comment
FOR EACH ROW
    EXECUTE PROCEDURE inc_comment_num();

-- trigger on tweet(like_num) --
CREATE OR REPLACE FUNCTION inc_comment_num1() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET comment_num = comment_num + 1 WHERE new.user_id = users.user_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementCommentNum1
AFTER INSERT ON comment
FOR EACH ROW
    EXECUTE PROCEDURE inc_comment_num1();

-- delete tweet(like_num) --
UPDATE tweet SET `comment_num` = `comment_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `comment_num` = `comment_num` - 1 WHERE deleted.user_id = users.user_id;

-- Actions and triggers in report --

-- trigger on users(like_num) --
CREATE OR REPLACE FUNCTION inc_report_num() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE users SET report_num = report_num + 1 WHERE new.user_id = users.user_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementReportNum
AFTER INSERT ON report
FOR EACH ROW
    EXECUTE PROCEDURE inc_report_num();

-- trigger on tweet(like_num) --
CREATE OR REPLACE FUNCTION inc_report_num1() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE tweet SET report_num = report_num + 1 WHERE new.tweet_id = tweet.tweet_id;
    RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER IncrementReportNum1
AFTER INSERT ON report
FOR EACH ROW
    EXECUTE PROCEDURE inc_report_num1();

-- delete tweet(like_num) --
UPDATE tweet SET `report_num` = `report_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `report_num` = `report_num` - 1 WHERE deleted.user_id = users.user_id;

-- delete users if report_num >= 100 --
DELETE FROM users WHERE report_num >= 100;