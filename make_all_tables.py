import csv
import pandas
import numpy as np
from collections import OrderedDict

df = pandas.read_csv('Tweet.csv')

all_users = list(df["writer"])
all_users = [str(x) for x in all_users]
tweet_counter = dict()
for tweet in all_users:
    tweet_counter[tweet] = tweet_counter.get(tweet, 0) + 1
tweet_counter = OrderedDict(sorted(tweet_counter.items()))

# print(tweet_counter)

follower_count = [0 for i in range(len(tweet_counter))]

f = open('followers.csv', 'w')
f.write('user_id1,user_id2')

num_of_users = len(tweet_counter)
avg_following = 21
p = avg_following/num_of_users
num_of_following = np.random.binomial(num_of_users, p, size=num_of_users)
for i in range(num_of_users):
    following = np.random.binomial(num_of_users, 0.5, size=num_of_following[i])
    for j in range(num_of_following[i]):
        f.write('\n' + str(i) + ',' + str(following[j]))
        follower_count[following[j]] += 1

f.close()

f = open('users.csv', 'w')
f.write('user_id,password,user_name,tweet_num,follower_num')

user_id = 0
for user in tweet_counter:
    f.write('\n' + str(user_id) + ',' + str(user_id) + ',' + user + ',' + str(tweet_counter[user]) + ',' + str(follower_count[user_id]))
    user_id += 1

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