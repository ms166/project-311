from flask import render_template, flash, redirect, url_for, request
from app import flask_app_instance
from flaskext.mysql import MySQL
from app.models import Food, Electronics, Clothes, Videogames, User, Cart, Sold
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

mysql_instance = MySQL(flask_app_instance)

@flask_app_instance.route('/')
@flask_app_instance.route('/homepage')
def homepage_view_func():
	createIfNotExists()
	insertDefaultProducts()
	return render_template('homepage.html', title='Home Page')



# ====================================
# Miscellaneous functions
# ====================================

def createIfNotExists():
	Food.create()
	Electronics.create()
	Clothes.create()
	Videogames.create()
	Cart.create()
	User.create()
	Sold.create()

def insertDefaultProducts():
	Food.insertDefault()
	Electronics.insertDefault()
	Clothes.insertDefault()
	Videogames.insertDefault()


# ====================================
# Admin view functions
# ====================================
@flask_app_instance.route('/admin_products', methods=['GET', 'POST'])
def admin_products_view_func():
	createIfNotExists()
	# insertDefaultProducts()

	print(f"args response: {request.args.to_dict()}")
	print(f"form response: {request.form.to_dict()}")

	request_type = request.form.get('request_type')

	if(request_type == 'update'):
		item_name = request.form.get('item_name')
		category = request.form.get('category')
		quantity = request.form.get('quantity')
		if(category.lower() == 'food'):
			Food.updateQuantity(item_name, quantity)
		elif(category.lower() == 'clothes'):
			Clothes.updateQuantity(item_name, quantity)
		elif(category.lower() == 'electronics'):
			Electronics.updateQuantity(item_name, quantity)
		else:
			assert category.lower() == 'videogames'
			Videogames.updateQuantity(item_name, quantity)

	if(request_type == 'add_new'):
		category = request.form.get('category')
		if(category.lower() == 'food'):
			item_name = request.form.get('name')
			quantity = request.form.get('quantity')
			price = request.form.get('price')
			weight = request.form.get('weight')
			expiry = request.form.get('expiry')
			Food.insertNew(item_name, quantity, price, weight, expiry)
		elif(category.lower() == 'electronics'):
			item_name = request.form.get('name')
			quantity = request.form.get('quantity')
			price = request.form.get('price')
			manufacturer = request.form.get('manufacturer')
			warranty = request.form.get('warranty')
			Electronics.insertNew(item_name, quantity, price, manufacturer, warranty)
		elif(category.lower() == 'clothes'):
			item_name = request.form.get('name')
			quantity = request.form.get('quantity')
			price = request.form.get('price')
			material = request.form.get('material')
			size = request.form.get('size')
			Clothes.insertNew(item_name, quantity, price, material, size)
		else:
			assert category.lower() == 'videogames'
			item_name = request.form.get('name')
			quantity = request.form.get('quantity')
			price = request.form.get('price')
			company = request.form.get('company')
			release_date = request.form.get('release_date')
			platform = request.form.get('platform')
			Videogames.insertNew(item_name, quantity, price, company, release_date, platform)


	food_rows = Food.getAll()
	food_columns = Food.getColumnNames()

	electronics_rows = Electronics.getAll()
	electronics_columns = Electronics.getColumnNames()

	clothes_rows = Clothes.getAll()
	clothes_columns = Clothes.getColumnNames()


	videogames_rows = Videogames.getAll()
	videogames_columns = Videogames.getColumnNames()
	return render_template('admin/admin_products.html', title='List of Products', food_rows=food_rows, food_columns=food_columns, electronics_rows=electronics_rows, electronics_columns=electronics_columns, clothes_rows=clothes_rows, clothes_columns=clothes_columns, videogames_rows=videogames_rows, videogames_columns=videogames_columns)


@flask_app_instance.route('/pending_purchases', methods=['GET', 'POST'])
def pending_purchases_view_func():
	createIfNotExists()

	print(f"args response: {request.args.to_dict()}")
	print(f"form response: {request.form.to_dict()}")

	Cart.update()
	item_name = request.form.get('item_name')
	if(item_name is not None):
		category = request.form.get('category')
		unit_price = request.form.get('unit_price')
		quantity = int(request.form.get('quantity'))
		if(category.lower() == 'food'):
			available = Food.getQuantity(item_name)
			Food.updateQuantity(item_name, -min(available, quantity))
			quantity = min(available, quantity)
		elif(category.lower() == 'clothes'):
			available = Clothes.getQuantity(item_name)
			Clothes.updateQuantity(item_name, -min(available, quantity))
			quantity = min(available, quantity)
		elif(category.lower() == 'electronics'):
			available = Electronics.getQuantity(item_name)
			Electronics.updateQuantity(item_name, -min(available, quantity))
			quantity = min(available, quantity)
		else:
			assert category.lower() == "videogames"
			available = Videogames.getQuantity(item_name)
			Videogames.updateQuantity(item_name, -min(available, quantity))
			quantity = min(available, quantity)
		print(item_name, quantity)
		Sold.insert(item_name, quantity, category, unit_price)
		Cart.delete(item_name, quantity)


	distinctUsers = Cart.distinctUsers()
	pending = {}
	for user in distinctUsers:
		pending[user] = Cart.getByUser(user[0])
	# for key in pending:
	# 	print(f'pending for {key[0]}:')
	# 	for j in pending[key]:
	# 		print(j)
	columns = Cart.getColumnNames()
	return render_template('admin/pending_purchases.html', title='Pending Purchases', distinctUsers=distinctUsers, pending=pending, columns=columns)

@flask_app_instance.route('/sales_analysis')
def sales_analysis_view_func():
	createIfNotExists()
	# insertDefaultProducts()

	food_sold = Sold.getFood()
	clothes_sold = Sold.getClothes()
	electronics_sold = Sold.getElectronics()
	videogames_sold = Sold.getVideogames()

	columns = Sold.columns()
	return render_template('admin/sales_analysis.html', title='Sales Analysis', columns=columns, food_sold=food_sold, clothes_sold=clothes_sold, electronics_sold=electronics_sold, videogames_sold=videogames_sold)

@flask_app_instance.route('/users_info')
def users_info_view_func():
	createIfNotExists()
	# insertDefaultProducts()

	user_to_delete = request.args.get('username')
	if(user_to_delete is not None):
		User.delete(user_to_delete)

	user_rows = User.getAll()
	user_columns = ['Username', 'Email', 'Total Spent']
	return render_template('admin/users_info.html', title='User Information', user_rows = user_rows, user_columns= user_columns)



# ====================================
# User view functions
# ====================================

@flask_app_instance.route('/all_products')
@login_required
def all_products_view_func():
	createIfNotExists()
	# insertDefaultProducts()

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
		if(category.lower() == 'food'):
			price = Food.getPrice(item_name)
		elif(category.lower() == 'electronics'):
			price = Electronics.getPrice(item_name)
		elif(category.lower() == 'videogames'):
			price = Videogames.getPrice(item_name)
		else:
			assert category.lower() == 'clothes'
			price = Clothes.getPrice(item_name)

		quantity = request.args.get('quantity')
		user = current_user.username
		Cart.insert(item_name, category, quantity, price, user)

	return render_template('users/all_products.html', title='All Products', food_rows=food_rows, food_columns=food_columns, electronics_rows=electronics_rows, electronics_columns=electronics_columns, clothes_rows=clothes_rows, clothes_columns=clothes_columns, videogames_rows=videogames_rows, videogames_columns=videogames_columns)


@flask_app_instance.route('/cart')
@login_required
def cart_view_func():
	createIfNotExists()

	item_to_delete = request.args.get('item_name')
	if(item_to_delete is not None):
		quantity = request.args.get('quantity')
		Cart.delete(item_to_delete, quantity)

	cart_rows = Cart.getByUser(current_user.username)
	cart_columns = Cart.getColumnNames()
	return render_template('users/cart.html', title='Cart', cart_rows=cart_rows, cart_columns=cart_columns)


@flask_app_instance.route('/clothes')
@login_required
def clothes_view_func():
	createIfNotExists()
	# insertDefaultProducts()

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
	createIfNotExists()
	# insertDefaultProducts()

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
	createIfNotExists()
	# insertDefaultProducts()

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

@flask_app_instance.route('/search', methods=['GET', 'POST'])
@login_required
def search_view_func():
	createIfNotExists()
	# insertDefaultProducts()

	# args_response = request.args.to_dict()
	# form_response = request.form.to_dict()
	# print(f"args response: {args_response}")
	# print(f"form response: {form_response}")

	item_name = request.args.get('item_name')
	quantity = request.args.get('quantity')
	queryFlag = False
	res = None
	if(item_name is not None and quantity is None and len(item_name) != 0): # search request
		queryFlag = True

		product_type = request.args.get('product_type')
		price_range = request.args.get('price_range')

		res_food = Food.searchQuery(item_name, price_range)
		res_clothes = Clothes.searchQuery(item_name, price_range)
		res_electronics = Electronics.searchQuery(item_name, price_range)
		res_videogames = Videogames.searchQuery(item_name, price_range)

		res = ()
		if(product_type == 'food'):
			res = res_food
		elif(product_type == 'clothes'):
			res = res_clothes
		elif(product_type == 'electronics'):
			res = res_electronics
		elif(product_type == 'videogames'):
			res = res_videogames
		else:
			assert product_type == 'all'
			if(res_food is not None):
				res = res + res_food
			if(res_clothes is not None):
				res = res + res_clothes
			if(res_electronics is not None):
				res = res + res_electronics
			if(res_videogames is not None):
				res = res + res_videogames
	elif(item_name is not None and len(item_name) != 0): # add to cart request
		queryFlag = True

		quantity = request.args.get('quantity') 
		category = request.args.get('category')
		if(category.lower() == 'food'):
			price = Food.getPrice(item_name)
		elif(category.lower() == 'clothes'):
			price = Clothes.getPrice(item_name)
		elif(category.lower() == 'electronics'):
			price = Electronics.getPrice(item_name)
		else:
			assert(category.lower() == 'videogames')
			price = Videogames.getPrice(item_name)
		user = current_user.username
		# print(item_name, quantity, price, category, user)
		Cart.insert(item_name, category, quantity, price, user)

	columns = ['Item Name', 'Quantity', 'Price', 'Category']
	return render_template('users/search.html', title='Search Products', queryFlag=queryFlag, res=res, columns=columns)

@flask_app_instance.route('/user_register', methods=['GET', 'POST'])
def user_register_view_func():
	createIfNotExists()
	# insertDefaultProducts()

	if(current_user.is_authenticated):
		return redirect(url_for('all_products_view_func'))
	form = RegistrationForm()
	if(form.validate_on_submit()):
		User.insert(form.username.data, form.email.data, form.password.data, 0)
		flash('You have been registered.')
		return redirect(url_for('user_sign_in_view_func'))
	return render_template('users/user_register.html', title='User Register', form=form)

@flask_app_instance.route('/user_sign_in', methods=['GET', 'POST'])
def user_sign_in_view_func():
	createIfNotExists()
	# insertDefaultProducts()

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
	createIfNotExists()
	# insertDefaultProducts()


	# print(f"args response: {request.args.to_dict()}")
	# print(f"form response: {request.form.to_dict()}")


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
