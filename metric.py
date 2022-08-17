from contextlib import ContextDecorator,contextmanager
import pymysql.cursors
from time import time

class DatabaseFactory():
	def __init__(self, host: str, user: str, password: str, database: str, port: int):
		self.host: str = host
		self.user: str = user
		self.password = password
		self.database: str = database
		self.port: int = port

	@contextmanager
	def connection(self):
		connection = self._connect()
		try:
			yield connection
		except Exception as ex:
			raise ex
		finally:
			connection.close()


	def _connect(self):
		return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            port=self.port,
        )

db = DatabaseFactory(
	host="127.0.0.1", 
	user="root", 
	password="", 
	database="metric",
	port=3306,
)

class Metric():
	def __init__(self, function: object): 

		self.function: object = function
		self.exec_time: float = None

	def __call__(self):
		t_start = time()
		self.function()
		t_end = time()
		
		self._metrics(self.function.__name__, t_end-t_start)

	def _metrics(self, function_name: str, execution_time: float):
		with db.connection() as connection: 
			with connection.cursor() as curs: 
				curs.execute("INSERT INTO metrics (function_name, execution_time) VALUES (%s, %s)", (function_name, execution_time*1000000))

		

