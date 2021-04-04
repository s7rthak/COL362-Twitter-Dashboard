make: db_test

db:
	sudo -u postgres psql db -f Data/build/drop.sql
	sudo -u postgres psql db -f Data/build/tables_constraints.sql
	sudo -u postgres psql db -f Data/build/copy_db.sql
	sudo -u postgres psql db -f Data/build/views.sql
	sudo -u postgres psql db -f Data/build/indexes.sql
	sudo -u postgres psql db -f Data/build/triggers.sql

db_test:
	sudo -u postgres psql db_test -f Data/build/drop.sql
	sudo -u postgres psql db_test -f Data/build/tables_constraints.sql
	sudo -u postgres psql db_test -f Data/build/triggers.sql
	sudo -u postgres psql db_test -f Data/build/copy_db_test.sql
	sudo -u postgres psql db_test -f Data/build/views.sql
	sudo -u postgres psql db_test -f Data/build/indexes.sql

check_db_test:
	sudo -u postgres psql db_test -f Data/build/check_db_test.sql

server:
	python3 app.py db

server_test:
	. venv/bin/activate && python3 app.py db_test

clean:
	sudo -u postgres psql db -f Data/build/drop.sql
	sudo -u postgres psql db_test -f Data/build/drop.sql