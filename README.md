# COL362 - MNCTwitter

## Project Proposal

Our project involves making a web-based application similar to twitter where users can post their opinions on top MNCs (Apple, Google Inc, Amazon, Tesla Inc, Microsoft).

We will include functionalities:

- [ ] Create/Delete account
- [ ] Posting new tweets (for 1 or more MNCs)/Deleting old tweets
- [ ] Follow/Unfollow users
- [ ] Like/Retweet/Comment on/Report tweets
- [ ] Reading tweets for (filtered) companies and see **new** comments on tweets
- [ ] Find recommended mutual followers
- [ ] Analysing the users own tweets, which were most liked/replied/etc
- [ ] Look at the trending graphs of companies
- [ ] Network analysis for followers

Assumptions: 

1. All users have 0 followers
2. No tweet has been reported
3. No current user have liked/retweeted/commented on any tweets

# Running the server on local machine

## Preparation

1. Install requirements:

   - postgresql

   - python3

   - python3-virtualenv

   ```
   sudo apt install python3-virtualenv
   ```

2. Create python virtual environment venv in the project directory

   ```
   virtualenv --no-site-packages venv
   ```

   If above command doesn't work try

   ```
   virtualenv venv
   ```

   Install dependencies in the virtual environment

   - Switch to virtual environment

     ```
     source venv/bin/activate
     ```

   - Install `flask` and `psycopg2` in venv environment

     ```
     pip install flask
     pip install psycopg2
     ```

     

3. Create new super user for postgres named "dbms_project" with password "dbms_project"

   ```
   sudo -u postgres createuser -s -i -d -r -l -w dbms_project
   sudo -u postgres psql -c "ALTER ROLE dbms_project WITH PASSWORD 'dbms_project';"
   ```

4. Create new databases with owner as the new user

   ```
   CREATE DATABASE db OWNER dbms_project;
   CREATE DATABASE db_test OWNER dbms_project;
   ```

## Execution

1. Making the CSV files: copy the `make_all_tables.py` file to the location where the original 3 .csv files are present and running the python file will generate the 8 needed csv files.

2. Connecting to Database:

   - Refresh original database

     ```
     make db
     ```

   - Refresh test database

     ```
     make db_test
     ```

   - To empty both the databases

     ```
     make clean
     ```

3. . Starting the server

   - With original database

     ```
     make server
     ```

   - With test database

     ```
     make server_test
     ```


## TODOs

- [ ] Triggers for all INSERTS that increment numbers (Test)
- [ ] Update make_all_tables.py
- [ ] Network Analysis
- [ ] Company Analysis

## Updates

- Remove id from (comment, tweet, user)
- Company names
- tweet_hash: single hashes instead of arrays
- user: New attribute follow_num
