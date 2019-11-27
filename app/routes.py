from flask import render_template, flash, redirect, url_for, request
from app import flask_app_instance
from flaskext.mysql import MySQL
mysql_instance = MySQL(flask_app_instance)

@flask_app_instance.route('/admin_base')
def admin_base_view_func():
	return render_template('admin_base.html', title='Admin Base Page')

@flask_app_instance.route('/admin_products', methods=['GET', 'POST'])
def admin_products_view_func():
	conn = mysql_instance.connect()
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS PRODUCTS(
			name varchar(30) not null primary key,
			price int not null,
			category varchar(30) not null,
			weight int not null
		);
		""")
	name = request.values.get('name')
	price = request.values.get('price')
	category = request.values.get('category')
	weight = request.values.get('weight')
	if(name and price and category and weight):
		price = int(price)
		weight = int(weight)
		cursor.execute(f"""
			INSERT INTO PRODUCTS(name, price, category, weight)
			VALUES('{name}', {price}, '{category}', {weight})
			""")

	cursor.execute("SELECT * FROM PRODUCTS")
	items = cursor.fetchall()
	conn.commit()
	return render_template('admin_products.html', title='Admin Products', items=items)

@flask_app_instance.route('/')
@flask_app_instance.route('/homepage')
def homepage_view_func():
	return render_template('homepage.html', title='Home Page')

@flask_app_instance.route('/user_base')	
def user_base_view_func():
	return render_template('user_base.html', title='User Base Page')

@flask_app_instance.route('/user_login', methods=['GET', 'POST'])
def user_login_page_view_func():
	conn = mysql_instance.connect()
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS USERS(
			username varchar(30) not null primary key,
			password varchar(30) not null
		);
		""")
	username = request.values.get('username')
	password = request.values.get('password')
	if(username and password):
		cursor.execute(f"""
			INSERT INTO USERS(username, password)
			VALUES('{username}', '{password}')
			""")

	cursor.execute("SELECT * FROM USERS")
	res = cursor.fetchall()
	conn.commit()
	return render_template('user_login_page.html', title='User Login', res=res)
