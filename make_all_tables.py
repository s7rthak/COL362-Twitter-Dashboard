import pandas
import numpy as np
from collections import OrderedDict
import re

df = pandas.read_csv('Tweet.csv')

# rewrite Tweet.csv
df["report_num"] = '0'
df["is_retweet"] = 'False'
df["original_tweet_id"] = ''
df['post_date'] = pandas.to_datetime(df['post_date'], unit='s')
df.to_csv('Tweet.csv', index=False)

all_users = list(df["writer"])
all_users = [str(x) for x in all_users]
tweet_counter = dict()
for tweet in all_users:
    tweet_counter[tweet] = tweet_counter.get(tweet, 0) + 1
tweet_counter = OrderedDict(sorted(tweet_counter.items()))

follower_count = [0 for i in range(len(tweet_counter))]

# Write follower.csv
f = open('follower.csv', 'w')
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

# Write users.csv
f = open('users.csv', 'w')
f.write('user_id,user_name,password,tweet_num,follower_num,comment_num,retweet_num,like_num,report_num')

user_id = 0
for user in tweet_counter:
    f.write('\n' + str(user_id) + ',' + user + ',' + str(user_id) + ',' + str(tweet_counter[user]) + ',' + str(follower_count[user_id]) + ',0,0,0,0')
    user_id += 1

f.close()

# Write favourite.csv
f = open('favourite.csv', 'w')
f.write('user_id,tweet_id')
f.close()

# Write comment.csv
f = open('comment.csv', 'w')
f.write('comment_id,user_id,tweet_id,comment_date,body')
f.close()

# Write report.csv
f = open('report.csv', 'w')
f.write('user_id,tweet_id')
f.close()

#Write tweet_hash.csv
def extract_hashtags(text):
    text = text.replace("'", " ")
    text = text.replace("#", " #")
    text = text.replace("http", " http")
    all_hashtags = list(set([re.sub(r"#+", "#", k) for k in set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in text.split() if i.startswith("#")])])]))
    all_hashtags = [hashtag[1:] for hashtag in all_hashtags]
    return all_hashtags

f = open('tweet_hash.csv', 'w')

for index, row in df.iterrows():
    f.write('\n' + str(row["tweet_id"]) + ',' + '"{' + ','.join(extract_hashtags(row["body"])) + '}"')

f.close()