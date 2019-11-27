import os

class Config:
	# this key is used by Flask and some of its extensions to generate 
	# a cryptograpic key
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisisagiantpassword'

	# MySQL config values
	MYSQL_DATABASE_HOST = 'localhost'
	MYSQL_DATABASE_PORT = 3306
	MYSQL_DATABASE_USER = 'root'
	MYSQL_DATABASE_PASSWORD = 'redSky123'
	MYSQL_DATABASE_DB = 'groceryDB'
