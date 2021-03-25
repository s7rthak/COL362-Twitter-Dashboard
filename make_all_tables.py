import csv
import pandas

df = pandas.read_csv('Tweet.csv')

all_users = set(df["writer"])
all_users = [str(x) for x in all_users]
all_users.sort()

# print(all_users)

f = open('users.csv', 'w')
f.write('user_id,password,user_name,follower_num')

for i in range(len(all_users)):
    f.write('\n' + str(i) + ',' + str(i) + ',' + all_users[i] + ',0')

f.close()

f = open('followers.csv', 'w')
f.write('user_id1,user_id2')
f.close()

f = open('favourite_tweet.csv', 'w')
f.write('user_id,tweet_id')
f.close()

f = open('comments.csv', 'w')
f.write('comment_id,user_id,tweet_id,comment_date,body')
f.close()

f = open('reports.csv', 'w')
f.write('user_id,tweet_id')
f.close()