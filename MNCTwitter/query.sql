-- Actions and triggers in tweet --

-- trigger on users(tweet_num) --
CREATE TRIGGER IncrementTweetNum 
AFTER INSERT ON tweet
REFERENCING
    NEW ROW AS nr
FOR EACH ROW 
BEGIN 
    UPDATE users SET `tweet_num` = `tweet_num` + 1 WHERE nr.writer = users.user_name
END;

-- INSERT into company_tweet --


-- trigger on tweet(retweet_num) -- 
CREATE TRIGGER IncrementRetweetNum
BEFORE INSERT ON tweet
REFERENCING 
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE tweet SET `retweet_num` = `retweet_num` + 1 WHERE nr.original_tweet_id = tweet.tweet_id
END;

-- trigger on user(retweet_num) --
CREATE TRIGGER IncrementRetweetNum1
AFTER INSERT ON tweet
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE users SET `retweet_num` = `retweet_num` + 1 WHERE nr.writer = users.user_name
END;

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
CREATE TRIGGER IncrementFollowerNum
AFTER INSERT ON follower
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE users SET `follower_num` = `follower_num` + 1 WHERE nr.user_id1 = users.user_id
END;

-- action on user(tweet_id, follower_num) -- 
UPDATE users SET `follower_num` = `follower_num` - 1 WHERE deleted.user_id1 = users.user_id

-- Actions and triggers in favourite --

-- trigger on users(like_num) --
CREATE TRIGGER IncrementLikeNum
AFTER INSERT ON favourite
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE users SET `like_num` = `like_num` + 1 WHERE nr.user_id = users.user_id
END;

-- trigger on tweet(like_num) --
CREATE TRIGGER IncrementLikeNum1
AFTER INSERT ON favourite
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE tweet SET `like_num` = `like_num` + 1 WHERE nr.tweet_id = tweet.tweet_id
END;

-- delete tweet(like_num) --
UPDATE tweet SET `like_num` = `like_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `like_num` = `like_num` - 1 WHERE deleted.user_id = users.user_id;

-- Actions and triggers in comment --

-- trigger on users(comment_num) --
CREATE TRIGGER IncrementCommentNum
AFTER INSERT ON comment
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE users SET `comment_num` = `comment_num` + 1 WHERE nr.user_id = users.user_id
END;

-- trigger on tweet(like_num) --
CREATE TRIGGER IncrementCommentNum2
AFTER INSERT ON comment
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE tweet SET `comment_num` = `comment_num` + 1 WHERE nr.tweet_id = tweet.tweet_id
END;

-- delete tweet(like_num) --
UPDATE tweet SET `comment_num` = `comment_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `comment_num` = `comment_num` - 1 WHERE deleted.user_id = users.user_id;

-- Actions and triggers in report --

-- trigger on users(like_num) --
CREATE TRIGGER IncrementReportNum
AFTER INSERT ON report
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE users SET `report_num` = `report_num` + 1 WHERE nr.user_id = users.user_id
END;

-- trigger on tweet(like_num) --
CREATE TRIGGER IncrementReportNum1
AFTER INSERT ON report
REFERENCING
    NEW ROW AS nr
FOR EACH ROW
BEGIN
    UPDATE tweet SET `report_num` = `report_num` + 1 WHERE nr.tweet_id = tweet.tweet_id
END;

-- delete tweet(like_num) --
UPDATE tweet SET `report_num` = `report_num` - 1 WHERE deleted.tweet_id = tweet.tweet_id;

-- delete users(like_num) --
UPDATE users SET `report_num` = `report_num` - 1 WHERE deleted.user_id = users.user_id;

-- delete users if report_num >= 100 --
DELETE FROM users WHERE report_num >= 100;