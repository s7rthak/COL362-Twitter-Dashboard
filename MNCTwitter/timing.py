import time
import psycopg2
import psycopg2.extensions
from psycopg2.extras import LoggingConnection, LoggingCursor
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MyLoggingCursor simply sets self.timestamp at start of each query                                                                 
class MyLoggingCursor(LoggingCursor):
	def execute(self, query, vars=None):
		self.timestamp = time.time()
		return super(MyLoggingCursor, self).execute(query, vars)

	def callproc(self, procname, vars=None):
		self.timestamp = time.time()
		return super(MyLoggingCursor, self).callproc(procname, vars)

# MyLogging Connection:                                                                                                             
#   a) calls MyLoggingCursor rather than the default                                                                                
#   b) adds resulting execution (+ transport) time via filter()                                                                     
class MyLoggingConnection(LoggingConnection):
	def filter(self, msg, curs):
		file = open('times.log', 'a')
		print(str(msg) + "   %s ms" % str((time.time() - curs.timestamp) * 1000), file = file)
		file.close()
		return str(msg) + "   %s ms" % str((time.time() - curs.timestamp) * 1000)

	def cursor(self, *args, **kwargs):
		kwargs.setdefault('cursor_factory', MyLoggingCursor)
		return LoggingConnection.cursor(self, *args, **kwargs)