-- *********************** CREATING TABLES *********************** 

CREATE TABLE tweet (
	tweet_id serial,
	writer text NOT NULL,
	post_date integer NOT NULL, -- timestamp type: integer  4 bytes  1901-12-13 to 2038-01-18
	body text NOT NULL,
	comment_num bigint NOT NULL,
	retweet_num bigint NOT NULL,
	like_num bigint NOT NULL,
	report_num bigint NOT NULL,
	is_retweet boolean NOT NULL,
	original_tweet_id bigint -- May have NULL values, the NULL value is separate from the idea of it being an FK
);

CREATE TABLE company_tweet (
	tweet_id bigint NOT NULL,
	ticker_symbol text NOT NULL
);

CREATE TABLE company (
	ticker_symbol text NOT NULL,
	company_name text NOT NULL
);

CREATE TABLE users (
	user_id serial,
	user_name text NOT NULL,
	password text NOT NULL,
	tweet_num bigint NOT NULL,
	follower_num bigint NOT NULL,
	comment_num bigint NOT NULL,
	retweet_num bigint NOT NULL,
	like_num bigint NOT NULL,
	report_num bigint NOT NULL
);

CREATE TABLE follower (
	user_id1 bigint NOT NULL,
	user_id2 bigint NOT NULL
);

CREATE TABLE favourite (
	user_id bigint NOT NULL,
	tweet_id bigint NOT NULL
);

CREATE TABLE comment (
	comment_id serial,
	user_id bigint,
	tweet_id bigint,
	comment_date integer, -- timestamp type: integer  4 bytes  1901-12-13 to 2038-01-18
	body text
);

CREATE TABLE report (
	user_id bigint,
	tweet_id bigint
);

CREATE TABLE tweet_hash (
	tweet_id int,
	hash text
);

-- *********************** CONSTRAINTS *********************** 

-- **** company ****
	-- Uniqueness constraints
	ALTER TABLE company add constraint ticker_symbol_unique UNIQUE (ticker_symbol);

-- **** users ****
	-- key constraints
	ALTER TABLE users add constraint user_id_key primary key (user_id);
	ALTER TABLE users add constraint user_id_unique UNIQUE (user_id);
	ALTER TABLE users add constraint user_name_unique UNIQUE (user_name);

	-- numbers
	ALTER TABLE users add constraint tweet_num_positive check (tweet_num >= 0);	
	ALTER TABLE users add constraint follower_num_positive check (follower_num >= 0);
	ALTER TABLE users add constraint comment_num_positive check (comment_num >= 0);
	ALTER TABLE users add constraint retweet_num_positive check (retweet_num >= 0);
	ALTER TABLE users add constraint like_num_positive check (like_num >= 0);
	ALTER TABLE users add constraint report_num_positive check (report_num >= 0);

-- **** company_tweet & tweet ****
	-- key constraints
	-- * company_tweet *
		ALTER TABLE company_tweet add constraint tweet_id_company_tweet_key primary key (tweet_id);
		ALTER TABLE company_tweet add constraint tweet_id_company_tweet_unique UNIQUE (tweet_id);

	-- * tweet *
		ALTER TABLE tweet add constraint tweet_id_tweet_key primary key (tweet_id);
		ALTER TABLE tweet add constraint tweet_id_tweet_unique UNIQUE (tweet_id);

	-- foreign key constraints
	-- * company_tweet *
		ALTER TABLE company_tweet add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id) on delete cascade;

	-- * tweet *
		ALTER TABLE tweet add constraint writer_ref foreign key (writer) references users(user_name);
		ALTER TABLE tweet add constraint original_tweet_id_ref foreign key (original_tweet_id) references tweet(tweet_id);

	-- numbers
	ALTER TABLE tweet add constraint comment_num_positive check (comment_num >= 0);
	ALTER TABLE tweet add constraint retweet_num_positive check (retweet_num >= 0);
	ALTER TABLE tweet add constraint like_num_positive check (like_num >= 0);
	ALTER TABLE tweet add constraint report_num_positive check (report_num >= 0);

	-- retweet
	ALTER TABLE tweet add constraint retweet_fields_valid check ((is_retweet AND original_tweet_id IS NOT NULL AND original_tweet_id <> tweet_id) OR (NOT is_retweet));

-- **** follower ****
	-- foreign key constraints
	ALTER TABLE follower add constraint user_id1_ref foreign key (user_id1) references users(user_id);
	ALTER TABLE follower add constraint user_id2_ref foreign key (user_id2) references users(user_id);

-- **** favourite ****
	-- foreign key constraints
	ALTER TABLE favourite add constraint user_id_ref foreign key (user_id) references users(user_id);
	ALTER TABLE favourite add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id) on delete cascade;

-- **** comment ****
	-- key constraints
	ALTER TABLE comment add constraint comment_id_key primary key (comment_id);
	ALTER TABLE comment add constraint comment_id_unique UNIQUE (comment_id);

	-- foreign key constraints
	ALTER TABLE comment add constraint user_id_comment_ref foreign key (user_id) references users(user_id);
	ALTER TABLE comment add constraint tweet_id_comment_ref foreign key (tweet_id) references tweet(tweet_id) on delete cascade;

-- **** report ****
	-- foreign key constraints
	ALTER TABLE report add constraint user_id_ref foreign key (user_id) references users(user_id);
	ALTER TABLE report add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id) on delete cascade;

-- **** tweet_hash ****
	-- foreign key constraints
	ALTER TABLE tweet_hash add constraint tweet_id_tweet_hash_ref foreign key (tweet_id) references tweet(tweet_id) on delete cascade;

\copy users(user_name, password, tweet_num, follower_num, comment_num, retweet_num, like_num, report_num) from 'Data/DB/users.csv' delimiter ',' csv header;
\copy company from 'Data/DB/company.csv' delimiter ',' csv header;
\copy tweet(writer, post_date, body, comment_num, retweet_num, like_num, report_num, is_retweet, original_tweet_id)  from 'Data/DB/tweet.csv' delimiter ',' csv header;
\copy company_tweet from 'Data/DB/company_tweet.csv' delimiter ',' csv header;
\copy follower from 'Data/DB/follower.csv' delimiter ',' csv header;
\copy favourite from 'Data/DB/favourite.csv' delimiter ',' csv header;
\copy comment(user_id, tweet_id, comment_date, body) from 'Data/DB/comment.csv' delimiter ',' csv header;
\copy report from 'Data/DB/report.csv' delimiter ',' csv header;