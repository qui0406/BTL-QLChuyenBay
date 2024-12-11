import datetime
import json, os
from QLChuyenBay import app, db
from QLChuyenBay.models import User, UserRole, Rule, AirPort, FlightRoute, FlightSchedule, BetweenAirport, Ticket, Customer
import hashlib
import re
import locale
locale.setlocale(locale.LC_ALL, 'vi_VN')

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
    return AirPort.query.filter().all()

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
            i_act= True,
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

def get_name_airport_by_id(id):
    return AirPort.query.filter(AirPort.id.__eq__(id)).first().name

def get_between_list(fs):
    bwa_list= BetweenAirport.query.filter(BetweenAirport.flight_sche_id.__eq__(fs.id)).all()
    airport_between_list = []
    if bwa_list:
        for bwa in bwa_list:
            obj = {
                'id': bwa.id,
                'airport_id': bwa.airport_id,
                'airport_name': get_name_airport_by_id(bwa.airport_id),
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
        'ticket1_book_quantity': fs.ticket1_book_quantity,
        'ticket2_book_quantity': fs.ticket2_book_quantity,
        'price_type_1': "{:,.0f}".format(fs.price_type_1),
        'price_type_2': "{:,.0f}".format(fs.price_type_2),
        'between_list': {
            'quantity': len(bwl),
            'data': bwl
        }
    }

def get_flight_sche_list():
    f_list = FlightSchedule.query.all()
    f_list.reverse()
    flight_sche_list = []
    for f in f_list:
        flight_sche = get_flight_sche_json(f.id)
        flight_sche_list.append(flight_sche)
    return flight_sche_list

def get_inp_search_json(departure_airport_id, departure_airport_name, arrival_airport_id,
                        arrival_airport_name, time_start, ticket_type):
    return {
        "departure_airport_id": departure_airport_id,
        "departure_airport_name": departure_airport_name,
        "arrival_airport_id": arrival_airport_id,
        "arrival_airport_name": arrival_airport_name,
        "time_start": time_start,
        "ticket_type": ticket_type
    }

def get_route_by_depart_and_arrival_id(departure_airport_id, arrival_airport_id):
    return FlightRoute.query.filter(FlightRoute.departure_airport_id.__eq__(departure_airport_id),
                                    FlightRoute.arrival_airport_id.__eq__(arrival_airport_id)).first()

def search_flight_sche(departure_airport_id, arrival_airport_id, time_start, ticket_type):
    time_array= time_start.split('-')
    time= datetime.datetime(int(time_array[0]), int(time_array[1]), int(time_array[2]))
    route= get_route_by_depart_and_arrival_id(departure_airport_id, arrival_airport_id)
    flight_list= FlightSchedule.query.filter(FlightSchedule.i_act.__eq__(True), FlightSchedule.i_del.__eq__(False)).all()

    flight_list_arr_tmp=[]

    for fl in flight_list:
        if fl.flight_route_id.__eq__(route.id) and fl.time_start.__gt__(time):
            flight_list_arr_tmp.append(fl)

    flight_list_arr=[]
    if int(ticket_type)==1:
        for fla in flight_list_arr_tmp:
            if fla.ticket1_quantity.__gt__(fla.ticket1_book_quantity):
                flight_list_arr.append(fla)
    if int(ticket_type)==2:
        for fla in flight_list_arr_tmp:
            if fla.ticket2_quantity.__gt__(fla.ticket2_book_quantity):
                flight_list_arr.append(fla)

    flight_schedule_list=[]
    for f in flight_list_arr:
        f_sche= get_flight_sche_json(f.id)
        flight_schedule_list.append(f_sche)
    return flight_schedule_list

def get_quantity_ticket():
    type_1= FlightSchedule.ticket1_quantity
    type_2= FlightSchedule.ticket2_quantity
    return type_1 + type_2

def get_ticket_json(t_id):
    t = Ticket.query.filter(Ticket.id.__eq__(t_id)).first()
    c = Customer.query.filter(Customer.id.__eq__(t.id)).first()
    return {
        'id': t.id,
        'author_id': t.author_id,
        'flight_sche_id': get_flight_sche_json(t.flight_sche_id),
        'ticket_price': t.ticket_price,
        'ticket_type': t.ticket_type,
        'ticket_package_price': t.ticket_package_price,
        'customer_name': c.customer_name,
        'customer_phone': c.customer_phone,
        'customer_id': c.customer_id,
        'created_at': t.created_at
    }

def get_ticket_list_json(user_id):
    t_list = Ticket.query.filter(Ticket.author_id.__eq__(user_id)).order_by(Ticket.created_at.desc()).all()
    t_list_json = []
    for t in t_list:
        t_list_json.append(get_ticket_json(t.id))
    return t_list_json


def get_ticket_remain(ticket_id, ticket_type):
    f= FlightSchedule.query.filter(FlightSchedule.i_act.__eq__(True), FlightSchedule.i_del.__eq__(False),
                                   FlightSchedule.id.__eq__(ticket_id)).first()
    remain=0
    if int(ticket_type)==1:
        remain= f.ticket1_quantity- f.ticket1_book_quantity
    if int(ticket_type)==2:
        remain = f.ticket2_quantity - f.ticket2_book_quantity
    return remain

def get_admin_rules_latest():
    ar = Rule.query.order_by(Rule.created_at.desc()).first()
    return ar

def check_time_ticket(f_id, is_user= True):
    f = FlightSchedule.query.filter(FlightSchedule.is_active.__eq__(True), FlightSchedule.is_deleted.__eq__(False),
                                    FlightSchedule.id.__eq__(f_id)).first()
    ar = get_admin_rules_latest()
    f_ts = f.time_start.timestamp()
    n_ts = datetime.datetime.now().timestamp()
    if is_user:
        return {
            'min': ar.time_book_ticket,
            'state': (f_ts - n_ts) / 3600 > ar.time_book_ticket
        }
    return {
        'min': ar.time_buy_ticket,
        'state': (f_ts - n_ts) / 3600 > ar.time_buy_ticket
    }



def get_user_by_id(user_id):
    return User.query.get(user_id)
