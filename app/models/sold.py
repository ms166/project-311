from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json


mysql_instance = MySQL(flask_app_instance)

class Sold():
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS SOLD(
				item_name varchar(30) NOT NULL PRIMARY KEY,
				quantity int NOT NULL,
				category varchar(30) NOT NULL,
				price int NOT NULL,
				FOREIGN KEY(item_name) REFERENCES ALL_PRODUCTS(item_name) ON UPDATE CASCADE ON DELETE CASCADE
			);
			""")

	def columns():
		return ['Item_name', 'Quantity', 'Unit Price']

	def getFood():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT item_name, quantity, price FROM SOLD
			WHERE category='food';
			""")
		res = cursor.fetchall()
		return res

	def getClothes():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT item_name, quantity, price FROM SOLD
			WHERE category='clothes';
			""")
		res = cursor.fetchall()
		return res
	def getElectronics():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT item_name, quantity, price FROM SOLD
			WHERE category='electronics';
			""")
		res = cursor.fetchall()
		return res
	def getVideogames():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT item_name, quantity, price FROM SOLD
			WHERE category='videogames';
			""")
		res = cursor.fetchall()
		return res
	def insert(item_name, quantity, category, price):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT * FROM SOLD WHERE item_name='{item_name}'
			""")
		res = cursor.fetchone()
		if(res is not None):
			cursor.execute(f"""
				UPDATE SOLD
				SET quantity = quantity + {quantity}
				WHERE item_name = '{item_name}';
				""")

		else:
			cursor.execute(f"""
				INSERT INTO SOLD(item_name, quantity, category, price)
				VALUES('{item_name}', {quantity}, '{category}', {price});
				""")
		conn.commit()