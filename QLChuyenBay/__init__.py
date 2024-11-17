from random import randint
import smtplib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
from flask_mail import *
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/qlchuyenbay?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.secret_key='jiugyvIU*YGUFT*&&^T&GUHBOHIGY&(*)(U*HIJBHVFYFY%^&^&^&(*)*YUGBHOIB48451'

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]= 587
app.config["MAIL_USERNAME"]='anhqui04062004@gmail.com'
app.config["MAIL_PASSWORD"]='hsesebwdzpkqnzna'
app.config["MAIL_USE_TLS"]= True

cloudinary.config(
    cloud_name= 'do43r8nr0',
    api_key='947875495844325',
    api_secret= 'evQEPk5TbxIMpCWbbXl8sLMbo6A'
)

otp= randint(000000, 999999)
mail=Mail(app=app)
db= SQLAlchemy(app=app)
login= LoginManager(app=app)