CREATE INDEX tweet_index ON tweet(tweet_id);

CREATE INDEX users_index ON users(user_id);

CREATE INDEX company_index ON company(ticker_symbol);

CREATE INDEX follower_index ON follower(user_id2);

CREATE INDEX company_tweet_index ON company_tweet(tweet_id);

CREATE INDEX favourite_index ON favourite(tweet_id);

CREATE INDEX comment_index ON comment(tweet_id);

CREATE INDEX report_index ON report(tweet_id);

CREATE INDEX tweet_hash_index ON tweet_hash(tweet_id);

CREATE INDEX popular_users_index ON popular_users(user_id);

CREATE INDEX popular_tweets_index ON popular_tweets(tweet_id);

CREATE INDEX popular_hashes_tweets_index ON popular_hashes_tweets(hash);