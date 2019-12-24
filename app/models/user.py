from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json


mysql_instance = MySQL(flask_app_instance)

@login_manager.user_loader
def load_user(user_id):
	User.create()
	return User.getByUsername(user_id)

	
class User(UserMixin):
	def insert(username, email, password, total_spent):
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
			INSERT INTO USERS(username, email, password_hash, total_spent)
			VALUES ('{username}', '{email}', '{generate_password_hash(password)}', {total_spent});
			""")
		conn.commit()

	def getAll():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT username, email, total_spent FROM USERS;
			""")
		res = cursor.fetchall()
		return res

	def delete(username):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			DELETE FROM USERS
			WHERE username = '{username}'
			""")
		conn.commit()

	def updateSpent(user, total_spent):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		print(f"""
			UPDATE USERS
			SET total_spent=total_spent+{total_spent}
			WHERE username = '{user}';
			""")
		cursor.execute(f"""
			UPDATE USERS
			SET total_spent=total_spent+{total_spent}
			WHERE username = '{user}';
			""")
		conn.commit()

	def create():
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS USERS(
				username varchar(50) NOT NULL PRIMARY KEY,
				email varchar(50) NOT NULL,
				password_hash varchar(128) NOT NULL,
				total_spent int NOT NULL
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
		username, email, password_hash, total_spent = userTuple
		return User(username, email, password_hash, total_spent)

	def getByEmail(email):
		conn = mysql_instance.connect()
		cursor = conn.cursor()
		cursor.execute(f"""
			SELECT * FROM USERS WHERE email = '{email}';
			""")
		userTuple = cursor.fetchone()
		if(userTuple is None):
			return None
		username, email, password_hash, total_spent = userTuple
		return User(username, email, password_hash, total_spent)

	def __init__(self, username, email, password_hash, total_spent):
		self.username = username
		self.email = email
		self.password_hash = password_hash
		self.total_spent = total_spent

	def get_id(self):
		return self.username

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)