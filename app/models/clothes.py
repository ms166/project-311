from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from .functions import computePriceRange

mysql_instance = MySQL(flask_app_instance)

class Clothes:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS CLOTHES(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(30) NOT NULL,
				quantity int NOT NULL,
				price int NOT NULL,
				material varchar(20) NOT NULL,
				size int NOT NULL 
			);
			""")

		cursor.execute("""
			ALTER TABLE CLOTHES AUTO_INCREMENT=3001;
			""")

	def getQuantity(item_name):
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		cursor.execute(f"""
			SELECT quantity FROM CLOTHES WHERE name = '{item_name}';
			""")
		ret = cursor.fetchone()
		return ret[0]

	def insertNew(name, quantity, price, material, size):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		try:
			cursor.execute(f"""
				SELECT * FROM CLOTHES
				WHERE name = '{name}';
				""")
			res = cursor.fetchone()
			if(res is not None):
				Clothes.updateQuantity(name, quantity)
				return
			cursor.execute(f"""
				INSERT INTO CLOTHES(name, quantity, price, material, size)
				VALUES('{name}', {quantity}, {price}, '{material}', {size});
				""")
			conn.commit()
		except Exception as e:
			raise(e)

	def updateQuantity(item_name, quantity):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			UPDATE CLOTHES
			SET quantity = quantity + {quantity}
			WHERE name = '{item_name}';
			""")
		cursor.execute(f"""
			DELETE FROM CLOTHES
			WHERE quantity <= 0;
			""")
		conn.commit()
	def searchQuery(item_name, price_range):
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		min_price, max_price = computePriceRange(price_range)

		cursor.execute(f"""
			SELECT name, quantity, price, 'clothes' as category
			FROM CLOTHES
			WHERE name like '%{item_name}%' AND price >= {min_price} AND price <= {max_price}
			ORDER BY price ASC;
			""")
		res = cursor.fetchall()
		return res # returns tuple of tuples

	def getPrice(item_name):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT price FROM CLOTHES WHERE name='{item_name}';
			""")
		price = cursor.fetchone()
		return price[0] # return price[0] because price is a tuple type

	def getColumnNames():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("DESCRIBE CLOTHES;")
		res = cursor.fetchall()
		names = []
		for i in res:
			names.append(i[0])
		return names

	def insertDefault():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		with open('app/default_tables/clothes.json') as file:
			clothes = json.load(file)
			for row in clothes:
				# change to round brackets
				line = str(row)
				line = list(line)
				line[0] = '('
				line[len(line) - 1] = ')'
				line = "".join(line)

				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM CLOTHES WHERE name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO CLOTHES(name, quantity, price, material, size)
					VALUES{line};
					""")
		conn.commit()
		conn.close()


	def getAll():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT * FROM CLOTHES; 
			""")
		rows = cursor.fetchall()
		return rows