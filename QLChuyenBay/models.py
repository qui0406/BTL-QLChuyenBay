from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from QLChuyenBay import db, login, app
from datetime import datetime
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
    __table_args__ = {'extend_existing': True}
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique= True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50), nullable= False, unique= True)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

class AirPort(BaseModel):
    __table_args__ = {'extend_existing': True}
    name= Column(String(100), nullable=False)
    # details= relationship('FlightRoute', backref='airport', lazy= True)

    def __str__(self):
        return self.name

# class FlightRoute(BaseModel):
#     __table_args__ = {'extend_existing': True}
#     airport_from_id= Column(Integer, ForeignKey(AirPort.id))
#     airport_to_id= Column(Integer, ForeignKey(AirPort.id))


# class Ticket(BaseModel):
#     __table_args__ = {'extend_existing': True}
#     ticket_price = Column(Integer, nullable= False)
#     ticket_type= Column(Integer, nullable= False)
#     ticket_package_price= Column(Integer, default=0)
#     created_at= Column(DateTime, default= datetime.now())
#
# class Customer(BaseModel):
#     __table_args__ = {'extend_existing': True}
#     customer_name= Column(String(100), nullable= False)
#     customer_email= Column(String(50))
#     customer_phone= Column(String(12), nullable= False)
#
#     def __str__(self):
#         return self.name

class Rule(BaseModel):
    __table_args__ = {'extend_existing': True}
    min_time_flight= Column(Float, default=30)
    max_quantity_between_airport= Column(Integer, default=2)
    min_time_stay_airport= Column(Float, default= 20)
    max_time_stay_airport= Column(Float, default= 30)
    time_book_ticket= Column(Float, default= 12)
    time_buy_ticket= Column(Float, default= 4)
    created_at= Column(DateTime, default= datetime.now())

# class FlightSchedule(BaseModel):
#     __table_args__ = {'extend_existing': True}
#     i_act= Column(Boolean, default= False)
#     i_del= Column(Boolean, default= False)
#
#     time_start= Column(Float, nullable= False)
#     time_end= Column(Float, nullable= False)
#     ticket1_quantity= Column(Integer, nullable= False)
#     ticket1_book_quantity= Column(Integer, default= 0)
#     ticket2_quantity= Column(Integer, nullable= False)
#     ticket2_book_quantity= Column(Integer, default= 0)
#     price= Column(Float, default=0)
#
#     # bw_airports = relationship('BetweenAirport', backref='FlightSchedule', lazy= True)
#
#     def __str__(self):
#         return str(self.id)
#
# class BetweenAirport(BaseModel):
#     __tablename__ = 'between_airport'
#     __table_args__ = {'extend_existing': True}
#     # airport_id = Column(Integer, ForeignKey(AirPort.id))
#     # flight_sche_id= Column(Integer, ForeignKey(FlightSchedule.id))
#     time_stay= Column(Float, nullable= False)
#     note= Column(String(100))
#     i_del= Column(Boolean, default= False)
#     is_deleted = Column(Boolean, default=False)

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)

if __name__=="__main__":
    with app.app_context():
        pass

        #db.create_all()
        # pass
        # a1 = AirPort(name="Tân Sơn Nhất")
        # a2 = AirPort(name="Nội Bài")
        # a3 = AirPort(name="Côn Đảo")
        # a4 = AirPort(name="Cà Mau")
        # a5 = AirPort(name="Cần Thơ")
        # a6 = AirPort(name="Phú Bài")
        # a7 = AirPort(name="Vân Đồn")
        # a8 = AirPort(name="Đà Nẵng")
        # a9 = AirPort(name="Phú Quốc")
        # a10 = AirPort(name="Vinh")
        #
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        # db.session.commit()
        # a = Rule()
        # db.session.add(a)
        # db.session.commit()