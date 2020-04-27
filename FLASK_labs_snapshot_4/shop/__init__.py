from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5adeede9bf4ab856ecead383d69a0d6ff12e5c1fd105bb5f'

#SPECIFY YOUR MYSQL CREDIENTIALS (USERNAME,MYSQL_PASSWORD and DATABASE_NAME) and uncomment:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:MYSQL_PASSWORD@csmysql.cs.cf.ac.uk:3306/DATABASE_NAME'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mssj67641497@localhost:3306/db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
