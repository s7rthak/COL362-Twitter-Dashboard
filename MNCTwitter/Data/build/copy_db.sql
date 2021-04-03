\timing
\copy users(user_name, password, tweet_num, follower_num, follow_num, comment_num, retweet_num, like_num, report_num) from 'Data/DB/users.csv' delimiter ',' csv header;
\copy company from 'Data/DB/company.csv' delimiter ',' csv header;
\copy tweet(writer_id, post_date, body, comment_num, retweet_num, like_num, report_num, is_retweet, original_tweet_id)  from 'Data/DB/tweet.csv' delimiter ',' csv header;
\copy company_tweet from 'Data/DB/company_tweet.csv' delimiter ',' csv header;
\copy follower from 'Data/DB/follower.csv' delimiter ',' csv header;
\copy favourite from 'Data/DB/favourite.csv' delimiter ',' csv header;
\copy comment(user_id, tweet_id, comment_date, body) from 'Data/DB/comment.csv' delimiter ',' csv header;
\copy report from 'Data/DB/report.csv' delimiter ',' csv header;