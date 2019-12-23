from flaskext.mysql import MySQL
from app import flask_app_instance, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

mysql_instance = MySQL(flask_app_instance)

def computePriceRange(price_range):
	min_price = max_price = 0
	if(price_range == 'order0-1'):
		min_price = 1
		max_price = 10
	elif(price_range == 'order1-2'):
		min_price = 10
		max_price = 100
	elif(price_range == 'order2-3'):
		min_price = 100
		max_price = 1000
	elif(price_range == 'order3-4'):
		min_price = 1000
		max_price = 10000
	else:
		assert price_range == 'all'
		min_price = 1
		max_price = 100000
	return min_price, max_price
