from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from sqlalchemy import create_engine
import pandas as pd


DB_VAR='postgresql://nwnuqchwcpcjss:7176f206a90a4161a0b7a4d1d74eb6c5f1c4382be315c7cc816cd9e034511f8c@ec2-52-31-217-108.eu-west-1.compute.amazonaws.com:5432/de5cnke41h2r55'

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_VAR
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

###Test if DB empty
class testdf():
    
    def __init__(self,table,DBURI):
        engine_local =create_engine(DBURI)
        
        df_in=pd.read_sql("SELECT * FROM {}".format(table),engine_local)
        self.test_val=df_in.shape[0]
        
        if self.test_val==0:
            self.test_bin=False
        else:
            self.test_bin=True
         
        engine_local.dispose()         
        
from webse import routes