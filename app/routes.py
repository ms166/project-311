from flask import render_template, flash, redirect, url_for, request
from app import flask_app_instance
from flaskext.mysql import MySQL
from app.models import Food, Electronics, Clothes, Videogames


mysql_instance = MySQL(flask_app_instance)

@flask_app_instance.route('/')
@flask_app_instance.route('/homepage')
def homepage_view_func():
	return render_template('homepage.html', title='Home Page')

# ====================================
# Admin view functions
# ====================================
@flask_app_instance.route('/admin_products')
def admin_products_view_func():
	Food.create()
	Electronics.create()
	Clothes.create()
	Videogames.create()

	Food.insertDefault()
	food_rows = Food.getAll()
	food_columns = Food.getColumnNames()

	Electronics.insertDefault()
	electronics_rows = Electronics.getAll()
	electronics_columns = Electronics.getColumnNames()
	return render_template('admin/admin_products.html', title='List of Products', food_rows=food_rows, food_columns=food_columns, electronics_rows=electronics_rows, electronics_columns=electronics_columns)


@flask_app_instance.route('/low_products')
def low_products_view_func():
	return render_template('admin/low_products.html', title='Products Low on Quantity')

@flask_app_instance.route('/sales_analysis')
def sales_analysis_view_func():
	return render_template('admin/sales_analysis.html', title='Sales Analysis')

@flask_app_instance.route('/scan')
def scan_view_func():
	return render_template('admin/scan.html', title='Scan Products')

@flask_app_instance.route('/users_info')
def users_info_view_func():
	return render_template('admin/users_info.html', title='User Information')



# ====================================
# User view functions
# ====================================

@flask_app_instance.route('/user_base')	
def user_base_view_func():
	return render_template('users/user_base.html', title='User Base Page')

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
	return render_template('users/user_login_page.html', title='User Login', res=res)
