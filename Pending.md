## ACTIONS and TRIGGERS

1. `tweet(tweet_id, writer, post_date, body, comment_num, retweet_num, like_num, report_num, is_retweet, original_tweet_id) `
   1. Posting new tweet: `INSERT INTO`
      Triggers:
      1. Increment `users(tweet_num)` 
      2. `INSERT INTO company_tweet(tweet_id, ticker_symbol)`
      3. If `is_retweet` then `UPDATE tweet(retweet_num)`
      4. If `is_retweet` then `UPDATE user(retweet_num)`
      5. `INSERT INTO tweet_hash(tweet_id...)`
   2. Deleting old tweet: `DELETE FROM`
      Triggers:
      1. Decrements `users(tweet_num)` 
      2. Those tweets that retweeted this tweet `DELETE FROM tweet(tweet_id)`
      3. `DELETE FROM company_tweet(tweet_id, ticker_symbol)`
      4. `DELETE FROM favourite(user_id, tweet_id)`
      5. `DELETE FROM comment(comment_id, user_id, tweet_id, comment_date, body)`
      6. `DELETE FROM report(user_id, tweet_id)`
      7. `DELETE FROM tweet_hash(tweet_id, hash)`
   3. Edit tweet
      Triggers:
      1. `UPDATE tweet_hash`
2. `company_tweet(tweet_id, ticker_symbol)`
3. `company(ticker_symbol, company_name)`
4. `users(user_id, user_name, password, tweet_num, follower_num, comment_num, retweet_num, like_num, report_num)`
   1. Add user
   2. Delete user
      Triggers:
      1. `DELETE FROM tweet`
      2. `DELETE FROM follower`
   3. Edit user
5. `follower(user_id1, user_id2)`  # User2 follows User1
   1. Add follower
      Triggers:
      1. `UPDATE users(tweet_id, follower_num)`
   2. Delete follower
      Triggers:
      1. `UPDATE users(tweet_id, follower_num)`
6. `favourite(user_id, tweet_id)`
   1. Add favourite
      Triggers:
      1. `UPDATE tweet(tweet_id, like_num)`
      2. `UPDATE users(user_id, like_num)`
   2. Delete favourite
      Triggers:
      1. `UPDATE tweet(tweet_id, like_num)`
      2. `UPDATE users(user_id, like_num)`
7. `comment(comment_id, user_id, tweet_id, comment_date, body)`
   1. Add comment
      Triggers:
      1. `UPDATE tweet(tweet_id, comment_num)`
      2. `UPDATE user(user_id, comment_num)`
   2. Delete comment
      Triggers:
      1. `UPDATE tweet(tweet_id, comment_num)`
      2. `UPDATE user(user_id, comment_num)`
   3. Edit comment
8. `report(user_id, tweet_id)` # If num_reports == 100 then we delete the tweet: TRIGGER
   1. Add report
      Triggers:
      1. `UPDATE tweet(tweet_id, report_num)`
      2. `UPDATE user(user_id, report_num)`
      3. On 100 delete tweet
   2. Delete report
      Triggers:
      1. `UPDATE tweet_data(tweet_id, report_num)`
      2. `UPDATE user_data(user_id, report_num)`
9. `tweet_hash(tweet_id, hash)`

## View

1. `user_recommendations(user_id1, user_id2, distance, priority = -4 * distance + 6 * popularity)`