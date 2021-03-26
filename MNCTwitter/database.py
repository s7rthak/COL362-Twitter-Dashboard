import psycopg2
from query import *

# **************** MANAGING DATABASE CONNECTIONS ****************

conn = None # Connection to PostgreSQL server
cur = None # Communication cursor to PostgreSQL

def connect(host, database, user, password):
	""" Connect to the PostgreSQL database server """
	print("Connecting to the PostgreSQL database...")

	try:
		global conn, cur

		# connect to the PostgreSQL server
		conn = psycopg2.connect(host=host, database=database, user=user, password=password)

		# create a cursor
		cur = conn.cursor()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def close():
	""" Closes connection to Database """
	# close the communication with the PostgreSQL
	if cur is not None:
		cur.close()
		print("Communication cursor with PostgreSQL closed.")

	# closing the connection to PostgreSQL
	if conn is not None:
		conn.close()
		print("Database connection closed.")


def check_user(username, password):
	""" Returns boolean if username, password is valid for a current user """
	cur.execute(check_user_query, (username, password))
	return cur.fetchone()[0]

def check_new_user(username, password, repassword):
	""" Returns error message if any on given inputs for new user """
	cur.execute(check_new_user_query, (username,))
	if not cur.fetchone()[0]:
		return "That username is taken. Try another."
	if password != repassword:
		return "Those passwords didn't match. Try again."
	cur.execute(insert_new_user_query, (username, password))
	conn.commit()

# execute a statement
# print('PostgreSQL database version:')
# cur.execute('SELECT * from tweet')
# db_version = cur.fetchall()
# print(db_version)