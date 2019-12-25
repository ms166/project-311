from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json


mysql_instance = MySQL(flask_app_instance)

class All_products:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS ALL_PRODUCTS(
				item_name varchar(30) NOT NULL PRIMARY KEY
			);
			""")
	def insertDefault():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		with open('app/default_tables/clothes.json') as file:
			clothes = json.load(file)
			for row in clothes:
				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM ALL_PRODUCTS WHERE item_name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO ALL_PRODUCTS(item_name)
					VALUES('{row[0]}');
					""")
		with open('app/default_tables/electronics.json') as file:
			electronics = json.load(file)
			for row in electronics:
				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM ALL_PRODUCTS WHERE item_name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO ALL_PRODUCTS(item_name)
					VALUES('{row[0]}');
					""")
		with open('app/default_tables/food.json') as file:
			food = json.load(file)
			for row in food:
				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM ALL_PRODUCTS WHERE item_name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO ALL_PRODUCTS(item_name)
					VALUES('{row[0]}');
					""")
		with open('app/default_tables/videogames.json') as file:
			videogames = json.load(file)
			for row in videogames:
				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM ALL_PRODUCTS WHERE item_name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO ALL_PRODUCTS(item_name)
					VALUES('{row[0]}');
					""")
		conn.commit()
		conn.close()

