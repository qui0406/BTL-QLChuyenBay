from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/qlchuyenbay?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.secret_key='jiugyvIU*YGUFT*&&^T&GUHBOHIGY&(*)(U*HIJBHVFYFY%^&^&^&(*)*YUGBHOIB48451'

cloudinary.config(
    cloud_name= 'do43r8nr0',
    api_key='947875495844325',
    api_secret= 'evQEPk5TbxIMpCWbbXl8sLMbo6A'
)

db= SQLAlchemy(app=app)
login= LoginManager(app=app)