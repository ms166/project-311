from flask import render_template, flash, redirect, url_for, request
from app import flask_app_instance
from flaskext.mysql import MySQL
from app.models import Food, Electronics, Clothes, Videogames, User
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user

mysql_instance = MySQL(flask_app_instance)

@flask_app_instance.route('/')
@flask_app_instance.route('/homepage')
def homepage_view_func():
	return render_template('homepage.html', title='Home Page')



# ====================================
# Miscellaneous functions
# ====================================





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

	Clothes.insertDefault()
	clothes_rows = Clothes.getAll()
	clothes_columns = Clothes.getColumnNames()


	Videogames.insertDefault()
	videogames_rows = Videogames.getAll()
	videogames_columns = Videogames.getColumnNames()
	return render_template('admin/admin_products.html', title='List of Products', food_rows=food_rows, food_columns=food_columns, electronics_rows=electronics_rows, electronics_columns=electronics_columns, clothes_rows=clothes_rows, clothes_columns=clothes_columns, videogames_rows=videogames_rows, videogames_columns=videogames_columns)


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

@flask_app_instance.route('/all_products')
def all_products_view_func():
	return render_template('users/all_products.html', title='All Products')

@flask_app_instance.route('/clothes')
def clothes_view_func():
	return render_template('users/clothes.html', title='Clothes')	

@flask_app_instance.route('/electronics')
def electronics_view_func():
	return render_template('users/electronics.html', title='Electronics')

@flask_app_instance.route('/food')
def food_view_func():
	return render_template('users/food.html', title='Food')

@flask_app_instance.route('/search')
def search_view_func():
	return render_template('users/search.html', title='Search Products')

@flask_app_instance.route('/user_register')
def user_register_view_func():
	return render_template('users/user_register.html', title='User Register')

@flask_app_instance.route('/user_sign_in', methods=['GET', 'POST'])
def user_sign_in_view_func():
	User.create()
	User.insertDummyUser()

	if(current_user.is_authenticated):
		return redirect(url_for('all_products_view_func'))
	form = LoginForm()

	if(form.validate_on_submit()):
		user = User.get(form.username.data)
		if(user is None or user.check_password(form.password.data) == False):
			flash('User does not exist.')
			return redirect(url_for('user_sign_in_view_func'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('all_products_view_func'))
	print('Not validated')
	return render_template('users/user_sign_in.html', title='Sign In', form = form)





@flask_app_instance.route('/user_sign_out')
def user_sign_out_view_func():
	logout_user()
	return redirect(url_for('user_sign_in_view_func'))
	
@flask_app_instance.route('/videogames')
def videogames_view_func():
	return render_template('users/videogames.html', title='Videogames')
