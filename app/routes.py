from flask import render_template, flash, redirect, url_for, request
from app import flask_app_instance
from flaskext.mysql import MySQL
from app.models import Food, Electronics, Clothes, Videogames, User, Cart
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

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
@login_required
def all_products_view_func():
	food_rows = Food.getAll()
	food_columns = Food.getColumnNames()

	electronics_rows = Electronics.getAll()
	electronics_columns = Electronics.getColumnNames()

	clothes_rows = Clothes.getAll()
	clothes_columns = Clothes.getColumnNames()

	videogames_rows = Videogames.getAll()
	videogames_columns = Videogames.getColumnNames()

	item_name = request.args.get('item_name')
	if(item_name is not None):
		# item_name, category, quantity, price, user
		category = request.args.get('category') 
		if(category == 'Food'):
			price = Food.getPrice(item_name)
		elif(category == 'Electronics'):
			price = Electronics.getPrice(item_name)
		elif(category == 'Videogames'):
			price = Videogames.getPrice(item_name)
		else:
			assert category == 'Clothes'
			price = Clothes.getPrice(item_name)

		quantity = request.args.get('quantity')
		user = current_user.username
		Cart.insert(item_name, category, quantity, price, user)

	return render_template('users/all_products.html', title='All Products', food_rows=food_rows, food_columns=food_columns, electronics_rows=electronics_rows, electronics_columns=electronics_columns, clothes_rows=clothes_rows, clothes_columns=clothes_columns, videogames_rows=videogames_rows, videogames_columns=videogames_columns)


@flask_app_instance.route('/cart')
@login_required
def cart_view_func():
	Cart.create()
	cart_rows = Cart.getByUser(current_user.username)
	cart_columns = Cart.getColumnNames()
	return render_template('users/cart.html', title='Cart', cart_rows=cart_rows, cart_columns=cart_columns)


@flask_app_instance.route('/clothes')
@login_required
def clothes_view_func():
	clothes_rows = Clothes.getAll()
	clothes_columns = Clothes.getColumnNames()

	item_name = request.args.get('item_name')
	if(item_name is not None):
		# item_name, category, quantity, price, user
		category = 'Clothes'
		quantity = request.args.get('quantity')
		price = Clothes.getPrice(item_name)
		user = current_user.username
		Cart.insert(item_name, category, quantity, price, user)

	return render_template('users/clothes.html', title='Clothes', clothes_rows=clothes_rows, clothes_columns=clothes_columns)	

@flask_app_instance.route('/electronics')
@login_required
def electronics_view_func():
	electronics_rows = Electronics.getAll()
	electronics_columns = Electronics.getColumnNames()

	item_name = request.args.get('item_name')
	if(item_name is not None):
		# item_name, category, quantity, price, user
		category = 'Electronics'
		quantity = request.args.get('quantity')
		price = Electronics.getPrice(item_name)
		user = current_user.username
		Cart.insert(item_name, category, quantity, price, user)

	return render_template('users/electronics.html', title='Electronics', electronics_rows=electronics_rows, electronics_columns=electronics_columns)

@flask_app_instance.route('/food')
@login_required
def food_view_func():
	food_rows = Food.getAll()
	food_columns = Food.getColumnNames()

	item_name = request.args.get('item_name')
	if(item_name is not None):
		# item_name, category, quantity, price, user
		category = 'Food'
		quantity = request.args.get('quantity')
		price = Food.getPrice(item_name)
		user = current_user.username
		Cart.insert(item_name, category, quantity, price, user)


	return render_template('users/food.html', title='Food', food_rows=food_rows, food_columns=food_columns)

@flask_app_instance.route('/search')
@login_required
def search_view_func():
	return render_template('users/search.html', title='Search Products')

@flask_app_instance.route('/user_register', methods=['GET', 'POST'])
def user_register_view_func():
	if(current_user.is_authenticated):
		return redirect(url_for('all_products_view_func'))
	form = RegistrationForm()
	if(form.validate_on_submit()):
		User.insert(form.username.data, form.email.data, form.password.data)
		flash('You have been registered.')
		return redirect(url_for('user_sign_in_view_func'))
	return render_template('users/user_register.html', title='User Register', form=form)

@flask_app_instance.route('/user_sign_in', methods=['GET', 'POST'])
def user_sign_in_view_func():
	User.create()

	if(current_user.is_authenticated):
		return redirect(url_for('all_products_view_func'))
	form = LoginForm()
	if(form.validate_on_submit()):
		user = User.getByUsername(form.username.data)
		if(user is None):
			flash('User does not exist.')
			return redirect(url_for('user_sign_in_view_func'))

		print(form.password.data)
		if(user.check_password(form.password.data) == False):
			flash('Wrong password.')
			return redirect(url_for('user_sign_in_view_func'))

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if(next_page is None):
			return redirect(url_for('user_sign_in_view_func'))
		return redirect(next_page)
	return render_template('users/user_sign_in.html', title='Sign In', form = form)





@flask_app_instance.route('/user_sign_out')
@login_required
def user_sign_out_view_func():
	logout_user()
	return redirect(url_for('user_sign_in_view_func'))
	
@flask_app_instance.route('/videogames', methods=['GET', 'POST'])
@login_required
def videogames_view_func():
	Cart.create() # create if not exists



	args_response = request.args.to_dict()
	form_response = request.form.to_dict()
	print(f"args response: {args_response}")
	print(f"form response: {form_response}")


	item_name = request.args.get('item_name')
	if(item_name is not None):
		quantity = request.args.get('quantity') 
		category = 'Videogames'
		price = Videogames.getPrice(item_name)
		user = current_user.username
		# print(item_name, quantity, price, category, user)
		Cart.insert(item_name, category, quantity, price, user)

	videogames_rows = Videogames.getAll()
	videogames_columns = Videogames.getColumnNames()
	return render_template('users/videogames.html', title='Videogames', videogames_rows=videogames_rows, videogames_columns=videogames_columns)
