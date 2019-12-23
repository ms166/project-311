from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json


mysql_instance = MySQL(flask_app_instance)

class Cart:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS CART(
				item_name varchar(30) NOT NULL, 
				category varchar(20) NOT NULL, 
				quantity int NOT NULL, 
				price int NOT NULL, 
				user varchar(50) NOT NULL,
				PRIMARY KEY(item_name, user)
			);
			""")

	def delete(item_name, quantity):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			UPDATE CART
			SET quantity = quantity - {quantity}
			WHERE item_name = '{item_name}';
			""")
		cursor.execute(f"""
			DELETE FROM CART
			WHERE quantity = 0;
			""")
		conn.commit();


	def getColumnNames():
		return ['item_name', 'category', 'quantity', 'Unit Price', 'Total Price']

	def getByUser(username):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f""" 
			SELECT item_name, category, quantity, price AS 'Unit Price', quantity * price AS 'Total Price'
			FROM CART WHERE user='{username}';
			""")
		res = cursor.fetchall()
		return res

	def insert(item_name, category, quantity, price, user):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"SELECT * FROM CART WHERE item_name='{item_name}' AND user='{user}' ;")
		product_already_in_cart = cursor.fetchone()
		if(product_already_in_cart is not None):
			cursor.execute(f"UPDATE CART SET quantity=quantity+{quantity} WHERE item_name='{item_name}' ;")
			conn.commit()
			return

		cursor.execute(f"""
			INSERT INTO CART(item_name, category, quantity, price, user)
			VALUES('{item_name}', '{category}', {quantity}, {price}, '{user}');
			""")
		conn.commit()
