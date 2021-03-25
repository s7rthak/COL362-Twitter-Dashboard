clean:
	sudo -u postgres psql db -f Data/build/drop.sql
	sudo -u postgres psql db_test -f Data/build/drop.sql

db: # Data/build/drop.sql Data/build/db_build.sql Data/DB/comment.csv Data/DB/company.csv Data/DB/company_tweet.csv Data/DB/favourite.csv Data/DB/follower.csv Data/DB/report.csv Data/DB/tweet.csv Data/DB/users.csv
	sudo -u postgres psql db -f Data/build/drop.sql
	sudo -u postgres psql db -f Data/build/db_build.sql

db_test: # Data/build/drop.sql Data/build/db_build_test.sql Data/DB_test/comment.csv Data/DB_test/company.csv Data/DB_test/company_tweet.csv Data/DB_test/favourite.csv Data/DB_test/follower.csv Data/DB_test/report.csv Data/DB_test/tweet.csv Data/DB_test/users.csv
	sudo -u postgres psql db_test -f Data/build/drop.sql
	sudo -u postgres psql db_test -f Data/build/db_build_test.sql

server:
	. venv/bin/activate && python3 app.py
