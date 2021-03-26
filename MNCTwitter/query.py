# **************** QUERIES ****************
check_user_query = "SELECT COUNT(*) = 1 FROM users WHERE user_name = %s AND password = %s;"

check_new_user_query = "SELECT count(*) = 0 FROM users WHERE user_name = %s;"

insert_new_user_query = "INSERT INTO users(user_id, user_name, password, tweet_num, follower_num, comment_num, retweet_num, like_num, report_num) VALUES(DEFAULT, %s, %s, 0, 0, 0, 0, 0, 0)"