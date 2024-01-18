import os
import sqlalchemy

db_name=os.environ.get("DATABASE_NAME")
user=os.environ.get("DATABASE_USER")
password=os.environ.get("DATABASE_PASSWORD")
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://"+user+":"+password+"@127.0.0.1:3306/"+db_name)