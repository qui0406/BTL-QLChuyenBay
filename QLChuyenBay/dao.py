import json, os
from QLChuyenBay import app, db
from QLChuyenBay.models import User, UserRole, Rule, AirPort, FlightRoute, FlightSchedule, BetweenAirport
import hashlib
import re

def add_user(name, username, password, email, **kwarg):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name = name, username = username, password = password,
                email = email, avatar = kwarg.get('avatar'))
    db.session.add(user)
    db.session.commit()

def check_secure_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    if re.match(pattern, password):
        return True

def auth_user(username, password, role=UserRole.USER):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password)).first()


def check_mail_exit(email):
    if email:
        return User.query.filter(User.email.__eq__(email)).first()


def override_password(email, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user= User.query.filter(User.email.__eq__(email)).first()
    if user:
        user.password= password
        db.session.commit()

def get_id_by_name_airport(name):

    return AirPort.query.filter(AirPort.name.__eq__(name)).first().id

def get_rule_admin():
    return Rule.query.order_by(Rule.created_at.desc()).first()

def save_admin_rules(min_time_flight, max_quantity_between_airport, min_time_stay_airport, max_time_stay_airport,
                     time_book_ticket,time_buy_ticket):
    sa= Rule(min_time_flight= min_time_flight,
             max_quantity_between_airport= max_quantity_between_airport,
             min_time_stay_airport= min_time_stay_airport,
             max_time_stay_airport= max_time_stay_airport,
             time_book_ticket= time_book_ticket
             ,time_buy_ticket= time_buy_ticket)
    db.session.add(sa)
    db.session.commit()
    return sa


def get_air_port_list():
    return AirPort.query.all()

def add_route_flight(departure_airport_id, arrival_airport_id):
    if departure_airport_id and arrival_airport_id:
        fr= FlightRoute(departure_airport_id= departure_airport_id,
                        arrival_airport_id= arrival_airport_id)
        db.session.add(fr)
        db.session.commit()
        return fr
    return None

def get_route_list():
    return FlightRoute.query.order_by(FlightRoute.created_date.desc()).all()

def del_route_id(route_id):
    fd= FlightRoute.query.filter(FlightRoute.id.__eq__(route_id)).first()
    db.session.delete(fd)
    db.session.commit()
    return fd

def create_flight_sche(depart_airport, arrival_airport, time_start, time_end,
                       quantity_1st_ticket, quantity_2nd_ticket, price_type_1, price_type_2):
    route_flight_id= FlightRoute.query.filter(FlightRoute.departure_airport_id.__eq__(depart_airport) and
                                              FlightRoute.arrival_airport_id.__eq__(arrival_airport)).first()
    if route_flight_id:
        f = FlightSchedule(
            flight_route_id=route_flight_id.id,
            time_start=time_start,
            time_end=time_end,
            ticket1_quantity=quantity_1st_ticket,
            ticket2_quantity=quantity_2nd_ticket,
            price_type_1=price_type_1,
            price_type_2=price_type_2)
        db.session.add(f)
        db.session.commit()
        return f
    return {
        'status': 500,
        'data': 'error'
    }

def create_between_airport(airport_id, flight_sche_id, time_stay, note):
    bwa= BetweenAirport(airport_id=int(airport_id), flight_sche_id=int(flight_sche_id), time_stay=float(time_stay),
                         note=note)
    db.session.add(bwa)
    db.session.commit()
    return bwa

def get_airport_by_id(a):
    return AirPort.query.filter(AirPort.id.__eq__(a)).first()

def get_route_json(fs):
    r= FlightRoute.query.filter(FlightRoute.id.__eq__(fs.flight_route_id)).first()

    if r:
        return {
            'departure_airport': get_airport_by_id(r.departure_airport_id).name,
            'arrival_airport': get_airport_by_id(r.arrival_airport_id).name
        }
    else:
        return {
            'departure_airport': '',
            'arrival_airport': ''
        }

def get_between_list(fs):
    bwa_list= BetweenAirport.query.filter(BetweenAirport.flight_sche_id.__eq__(fs.id)).all()
    airport_between_list = []
    if bwa_list:
        for bwa in bwa_list:
            obj = {
                'id': bwa.id,
                'airport_id': bwa.airport_id,
                'flight_sche_id': bwa.flight_sche_id,
                'time_stay': bwa.time_stay,
                'note': bwa.note
            }
            airport_between_list.append(obj)
    else:
        obj = {
            'id': '',
            'airport_id': '',
            'flight_sche_id': '',
            'time_stay': '',
            'note': ''
        }
        airport_between_list.append(obj)
    return airport_between_list

def get_flight_sche_json(id):
    fs= FlightSchedule.query.filter(FlightSchedule.id.__eq__(id)).first()
    fr= get_route_json(fs)
    bwl= get_between_list(fs)

    return {
        "id": fs.id,
        'departure_airport': fr['departure_airport'],
        'arrival_airport': fr['arrival_airport'],
        'time_start': fs.time_start,
        'time_end': fs.time_end,
        'ticket1_quantity': fs.ticket1_quantity,
        'ticket2_quantity': fs.ticket2_quantity,
        'price_type_1':fs.price_type_1,
        'price_type_2': fs.price_type_2,
        'between_list': bwl
    }

def get_flight_sche_list():
    f_list = FlightSchedule.query.all()
    f_list.reverse()
    flight_sche_list = []
    for f in f_list:
        flight_sche = get_flight_sche_json(f.id)
        flight_sche_list.append(flight_sche)
    return flight_sche_list

def get_user_by_id(user_id):
    return User.query.get(user_id)
