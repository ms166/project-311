from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request

url = "http://127.0.0.1:5000/user_sign_in?next=%2Ffood"
print(url_parse())