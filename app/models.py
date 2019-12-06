from flaskext.mysql import MySQL
from app import flask_app_instance

mysql_instance = MySQL(flask_app_instance)

# column-name data-type not-null default auto-increment constraints 

class Food:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS FOOD(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(20) NOT NULL,
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
		cursor.execute("SELECT name FROM FOOD WHERE name='Asparagus';")
		res = cursor.fetchall()

		if(len(res) != 0):
			return

		cursor.execute("""
			INSERT INTO FOOD(name, quantity, price, weight, expiry)
			VALUES 
				('Asparagus', 10, 100, 300, CURDATE()),
				('Apple', 18, 100, 50, CURDATE()),
				('Orange', 23, 120, 20, CURDATE()),
				('Banana', 50, 105, 23, CURDATE()),
				('Sprouts', 60, 120, 234, CURDATE()),
				('Beans', 40, 190, 421, CURDATE()),
				('Tomato', 45, 300, 111, CURDATE()),
				('Corn', 77, 180, 150, CURDATE()),
				('Celery', 12, 289, 160, CURDATE()),
				('Mango', 190, 76, 140, CURDATE()),
				('Papaya', 200, 99, 120, CURDATE()),
				('Olives', 300, 11, 110, CURDATE());
			""")
		conn.commit()

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
				name varchar(20) NOT NULL,
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
		cursor.execute("SELECT name FROM ELECTRONICS WHERE name='Headphones WH1000XM3';")
		res = cursor.fetchall()

		if(len(res) != 0):
			return

		cursor.execute("""
			INSERT INTO ELECTRONICS(name, quantity, price, manufacturer, warranty)
			VALUES 
				('Headphones WH1000XM3', 10, 1000, 'Sony', True),
				('Beats Solo3', 10, 299, 'Beats', False),
				('Apple Watch Series 5', 1, 500, 'Apple', True),
				('Samsumg Evo U3', 7, 100, 'Samsung', True),
				('Sandisk microSD', 9, 300, 'Sandisk', False),
				('DeathAdder Mouse', 12, 2000, 'Razer', False),
				('Earpods', 13, 1000, 'Apple', True),
				('Keyboard', 13, 400, 'Logitech', False),
				('Charge pad', 10, 300, 'Mophie', False),
				('Bluetooth Speaker', 2, 200, 'Nixplay', True);
			""")
		conn.commit()

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
				name varchar(20) NOT NULL,
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

class Videogames:
	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS VIDEOGAMES(
				item_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				name varchar(20) NOT NULL,
				quantity int NOT NULL,
				price int NOT NULL,
				company varchar(20) NOT NULL,
				release_date DATE NOT NULL,
				OS varchar(20) NOT NULL
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
