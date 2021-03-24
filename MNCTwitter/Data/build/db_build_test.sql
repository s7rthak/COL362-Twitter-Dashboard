-- *********************** CREATING TABLES *********************** 

CREATE TABLE tweet (
	tweet_id bigint NOT NULL,
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
	user_id text NOT NULL,
	password text NOT NULL,
	tweet_num bigint NOT NULL,
	follower_num bigint NOT NULL
);

CREATE TABLE follower (
	user_id1 text NOT NULL,
	user_id2 text NOT NULL
);

CREATE TABLE favourite (
	user_id text NOT NULL,
	tweet_id bigint NOT NULL
);

CREATE TABLE comment (
	comment_id bigint,
	user_id text,
	tweet_id bigint,
	comment_date integer, -- timestamp type: integer  4 bytes  1901-12-13 to 2038-01-18
	body text
);

CREATE TABLE report (
	user_id text,
	tweet_id bigint
);

-- *********************** CONSTRAINTS *********************** 

-- **** company ****
	-- Uniqueness constraints
	ALTER TABLE company add constraint ticker_symbol_unique UNIQUE (ticker_symbol);

-- **** users ****
	-- key constraints
	ALTER TABLE users add constraint user_id_key primary key (user_id);
	ALTER TABLE users add constraint user_id_unique UNIQUE (user_id);

	-- numbers
	ALTER TABLE users add constraint tweet_num_positive check (tweet_num >= 0);	
	ALTER TABLE users add constraint follower_num_positive check (follower_num >= 0);

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
		ALTER TABLE company_tweet add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id);

	-- * tweet *
		ALTER TABLE tweet add constraint writer_ref foreign key (writer) references users(user_id);
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
	ALTER TABLE favourite add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id);

-- **** comment ****
	-- key constraints
	ALTER TABLE comment add constraint comment_id_key primary key (comment_id);
	ALTER TABLE comment add constraint comment_id_unique UNIQUE (comment_id);

	-- foreign key constraints
	ALTER TABLE comment add constraint user_id_ref foreign key (user_id) references users(user_id);
	ALTER TABLE comment add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id);

-- **** report ****
	-- foreign key constraints
	ALTER TABLE report add constraint user_id_ref foreign key (user_id) references users(user_id);
	ALTER TABLE report add constraint tweet_id_ref foreign key (tweet_id) references tweet(tweet_id);

\copy users from './DB_test/users.csv' delimiter ',' csv header;
\copy company from './DB_test/company.csv' delimiter ',' csv header;
\copy tweet from './DB_test/tweet.csv' delimiter ',' csv header;
\copy company_tweet from './DB_test/company_tweet.csv' delimiter ',' csv header;
\copy follower from './DB_test/follower.csv' delimiter ',' csv header;
\copy favourite from './DB_test/favourite.csv' delimiter ',' csv header;
\copy comment from './DB_test/comment.csv' delimiter ',' csv header;
\copy report from './DB_test/report.csv' delimiter ',' csv header;