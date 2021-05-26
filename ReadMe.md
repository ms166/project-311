# Usage
* `cd grocery-store-flask-app`
* Install dependencies: `cat requirements.txt | xargs -n 1 pip install`
* `export FLASK_APP=flaskapp.py`
* Set up a MySQL server and create a database named `groceryDB` by running `CREATE DATABASE groceryDB;` in the mysql prompt. If you want to name it something else, then change the `MYSQL_DATABASE_DB` parameter in the `grocery-store-flask-app/config.py` file. Configuration variables such as MySQL ports, passwords and DB names can also be changed in this file.
* Start application: `flask run`
* go to `http://127.0.0.1:5000/`
