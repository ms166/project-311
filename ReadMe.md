# Current Progress
Pretty much nothing has been done yet. The app only allows inserting values into a table which is displayed back on the page.
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
* You must be in the project-311 directory to execute all the subsequent commands.
* Install the extensions required for this app:
  * The file `requirements.txt` contains a list of all the required python packages
  * After changing to the project-311 directory, install all requried packages by typing:   
        `pip install -r requirements.txt`
  * More info: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
* Set flask environment variable by typing:
  * Unix: `export FLASK_APP=project311.py`
  * Windows: `set FLASK_APP=project311.py`
* Typing `flask run` should now start a flask server. The app should be running on `http://127.0.0.1:5000/`. But the mysql server still has to be set up.
* Set up a MySQL server:
  * Install mysql on your system
  * Open the `project-311/config.py file` and change the parameters appropriately.
  * Start a MySQL server
* Run the program:
  * type: `flask run`
  * go to `http://127.0.0.1:5000/`
