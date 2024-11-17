from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from QLChuyenBay import db, login
from datetime import datetime
from QLChuyenBay import app
from enum import Enum as UserEnum
import dao
from flask_login import login_user
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__= True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    STAFF = 2
    USER = 3

class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique= True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__=="__main__":
    with app.app_context():
        db.create_all()


