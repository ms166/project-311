from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from .functions import computePriceRange


mysql_instance = MySQL(flask_app_instance)

class Videogames:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS VIDEOGAMES(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(30) NOT NULL,
				quantity int NOT NULL,
				price int NOT NULL,
				company varchar(20) NOT NULL,
				release_date DATE NOT NULL,
				platform varchar(30) NOT NULL
			);
			""")
		cursor.execute("""
			ALTER TABLE VIDEOGAMES AUTO_INCREMENT=4001;
			""")

	def getQuantity(item_name):
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		cursor.execute(f"""
			SELECT quantity FROM VIDEOGAMES WHERE name = '{item_name}';
			""")
		ret = cursor.fetchone()
		if(ret is None):
			ret = 0
		else:
			ret = ret[0]
		return ret

	def insertNew(name, quantity, price, company, release_date, platform):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		try:
			cursor.execute(f"""
				SELECT * FROM VIDEOGAMES
				WHERE name = '{name}';
				""")
			res = cursor.fetchone()
			if(res is not None):
				Videogames.updateQuantity(name, quantity)
				return
			cursor.execute(f"""
				INSERT INTO VIDEOGAMES(name, quantity, price, company, release_date, platform)
				VALUES('{name}', {quantity}, {price}, '{company}', '{release_date}', '{platform}');
				""")
			conn.commit()
		except Exception as e:
			raise(e)

	def updateQuantity(item_name, quantity):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			UPDATE VIDEOGAMES
			SET quantity = quantity + {quantity}
			WHERE name = '{item_name}';
			""")
		cursor.execute(f"""
			DELETE FROM VIDEOGAMES
			WHERE quantity <= 0;
			""")
		conn.commit()

	def searchQuery(item_name, price_range):
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		min_price, max_price = computePriceRange(price_range)

		cursor.execute(f"""
			SELECT name, quantity, price, 'videogames' as category
			FROM VIDEOGAMES
			WHERE name like '%{item_name}%' AND price >= {min_price} AND price <= {max_price}
			ORDER BY price ASC;
			""")
		res = cursor.fetchall()
		return res # returns tuple of tuples

	def getColumnNames():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("DESCRIBE VIDEOGAMES;")
		res = cursor.fetchall()
		names = []
		for i in res:
			names.append(i[0])
		return names
	
	def insertDefault():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		with open('app/default_tables/videogames.json') as file:
			videogames = json.load(file)
			for row in videogames:
				# change to round brackets
				line = str(row)
				line = list(line)
				line[0] = '('
				line[len(line) - 1] = ')'
				line = "".join(line)

				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM VIDEOGAMES WHERE name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO VIDEOGAMES(name, quantity, price, company, release_date, platform)
					VALUES{line};
					""")
		conn.commit()
		conn.close()


	def getPrice(name):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT price FROM VIDEOGAMES WHERE name = '{name}';
			""")
		price = cursor.fetchone()
		return price[0]

	def getAll():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT * FROM VIDEOGAMES;
			""")
		rows = cursor.fetchall()
		return rows