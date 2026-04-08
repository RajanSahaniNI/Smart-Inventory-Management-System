import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    # Based on a previous conversation where 'rajan123@' was used as the MySQL password
    MYSQL_PASSWORD = 'rajan123@' 
    MYSQL_DB = 'inventory_db'
