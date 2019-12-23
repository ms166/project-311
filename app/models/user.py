@login_manager.user_loader
def load_user(user_id):
	User.create()
	return User.getByUsername(user_id)

	
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
			VALUES ('{username}', '{email}', '{generate_password_hash(password)}');
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