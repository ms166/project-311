# Current Progress
* 28/11/2019:
  * Pretty much nothing has been done yet. The app only allows inserting values into a table which is displayed back on the page.
* 06/12/2019: 
  * Made separtions for admin pages and user pages
  * Added products table with default values.
  * Added CSS files for sidebar and products table. Taken from
  https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_sidenav_fixed
  and 
  https://www.w3schools.com/html/tryit.asp?filename=tryhtml_table_intro
  * Note about CSS: after making changes to CSS files, for the changes to be shown, cookies and cache must be cleared.

# Installation
* Install python 3 on your system
* Create a virtual environment in any directory:
  * Unix: `python3 -m tutorial-env` 
  * Windows: probably the same as Unix.
  * More info: https://docs.python.org/3/tutorial/venv.html
* Activate the virtual environment:
  * Unix: `source tutorial-env/bin/activate`
  * Windows: `tutorial-env\Scripts\activate.bat`
  * More info: https://docs.python.org/3/tutorial/venv.html
* You must be in the `project-311` directory to execute all the subsequent commands.
* Install the extensions required for this app:
  * The file `requirements.txt` contains a list of all the required python packages
  * Install all requried packages by typing:   
        `pip install -r requirements.txt`
  * More info: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
* Set flask environment variable by typing:
  * Unix: `export FLASK_APP=project311.py`
  * Windows: `set FLASK_APP=project311.py`
* Typing `flask run` should now start a flask server. The app should be running on `http://127.0.0.1:5000/`. But the mysql server still has to be set up.
* Set up a MySQL server:
  * Install mysql on your system
  * Open the `project-311/config.py` file and change the parameters appropriately.
  * Start a MySQL server
  * Create a database named `groceryDB`. If you name it something else, then change the `MYSQL_DATABASE_DB` parameter in the `project-311/config.py` file.
  * Change paramters in `the project-311/config.py` file if you need to change configuration variables such as MySQL ports, passwords, db names etc.
* Run the program:
  * type: `flask run`
  * go to `http://127.0.0.1:5000/`
