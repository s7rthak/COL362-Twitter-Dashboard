\copy users(user_name, password, tweet_num, follower_num, follow_num, comment_num, retweet_num, like_num, report_num) from 'Data/DB_test/users.csv' delimiter ',' csv header;
\copy company from 'Data/DB_test/company.csv' delimiter ',' csv header;
\copy tweet(writer_id, post_date, body, comment_num, retweet_num, like_num, report_num, is_retweet, original_tweet_id)  from 'Data/DB_test/tweet.csv' delimiter ',' csv header;
\copy company_tweet from 'Data/DB_test/company_tweet.csv' delimiter ',' csv header;
\copy follower from 'Data/DB_test/follower.csv' delimiter ',' csv header;
\copy favourite from 'Data/DB_test/favourite.csv' delimiter ',' csv header;
\copy comment(user_id, tweet_id, comment_date, body) from 'Data/DB_test/comment.csv' delimiter ',' csv header;
\copy report from 'Data/DB_test/report.csv' delimiter ',' csv header;
\copy tweet_hash from 'Data/DB_test/tweet_hash.csv' delimiter ',' csv header;