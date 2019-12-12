from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

mysql_instance = MySQL(flask_app_instance)

# column-name data-type not-null default auto-increment constraints
@login_manager.user_loader
def load_user(user_id):
	return User.getByUsername(user_id)


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


class User(UserMixin):
	def insert(username, email, password):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT * 
			FROM USERS 
			WHERE username='{username}' OR email = '{email}'
			;
			""")
		res = cursor.fetchone()
		if(res is not None):
			raise(Exception('User already exists.'))
		cursor.execute(f"""
			INSERT INTO USERS(username, email, password_hash)
			VALUES ('{username}', '{email}', '{generate_password_hash("password")}');
			""")
		conn.commit()


	def printUsers():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT * 
			FROM USERS 
			;
			""")
		res = cursor.fetchall()
		for i in res:
			print(i)

	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS USERS(
				username varchar(50) NOT NULL PRIMARY KEY,
				email varchar(50) NOT NULL,
				password_hash varchar(128) NOT NULL 
			);
			""")

	def getByUsername(username):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT * FROM USERS WHERE username = '{username}';
			""")
		userTuple = cursor.fetchone()
		if(userTuple is None):
			return None
		username, email, password_hash = userTuple
		return User(username, email, password_hash)

	def getByEmail(email):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT * FROM USERS WHERE email = '{email}';
			""")
		userTuple = cursor.fetchone()
		if(userTuple is None):
			return None
		username, email, password_hash = userTuple
		return User(username, email, password_hash)

	def __init__(self, username, email, password_hash):
		self.username = username
		self.email = email
		self.password_hash = password_hash

	def get_id(self):
		return self.username

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Food:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS FOOD(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(30) NOT NULL,
				quantity int NOT NULL,
				price int NOT NULL,
				weight int NOT NULL,
				expiry DATE NOT NULL
			);
			""")
		cursor.execute("""
			ALTER TABLE FOOD AUTO_INCREMENT=1001;
			""")

	def getColumnNames():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("DESCRIBE FOOD;")
		res = cursor.fetchall()
		names = []
		for i in res:
			names.append(i[0])
		return names

	def insertDefault():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		with open('app/default_tables/food.json') as file:
			foods = json.load(file)
			for row in foods:
				# change to round brackets
				line = str(row)
				line = list(line)
				line[0] = '('
				line[len(line) - 1] = ')'
				line = "".join(line)

				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM FOOD WHERE name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO FOOD(name, quantity, price, weight, expiry)
					VALUES{line};
					""")
		conn.commit()
		conn.close()
	

	def getAll():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT * FROM FOOD; 
			""")
		rows = cursor.fetchall()
		return rows


class Electronics:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS ELECTRONICS(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(30) NOT NULL,
				quantity int NOT NULL,
				price int NOT NULL,
				manufacturer varchar(20) NOT NULL,
				warranty boolean 
			);
			""")

		cursor.execute("""
			ALTER TABLE ELECTRONICS AUTO_INCREMENT=2001;
			""")

	def getColumnNames():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("DESCRIBE ELECTRONICS;")
		res = cursor.fetchall()
		names = []
		for i in res:
			names.append(i[0])
		return names


	def insertDefault():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		with open('app/default_tables/electronics.json') as file:
			electronics = json.load(file)
			for row in electronics:
				# change to round brackets
				line = str(row)
				line = list(line)
				line[0] = '('
				line[len(line) - 1] = ')'
				line = "".join(line)

				# check if it already exists
				cursor.execute(f"""
					SELECT * FROM ELECTRONICS WHERE name='{row[0]}';
					""")
				ret = cursor.fetchone()
				if(ret is not None):
					continue

				# insert if it doesn't already exist
				cursor.execute(f"""
					INSERT INTO ELECTRONICS(name, quantity, price, manufacturer, warranty)
					VALUES{line};
					""")
		conn.commit()
		conn.close()

	def getAll():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT * FROM ELECTRONICS; 
			""")
		rows = cursor.fetchall()
		return rows

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