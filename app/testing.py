import os
from config import Config
user = {'one' : 1, 'two' : '2'}


print("this is the testing file")
print(f"{os.environ.get('SECRET_KEY')} is the env variable")
print(f"{Config.SECRET_KEY} is the key")