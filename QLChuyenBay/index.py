import stripe
from QLChuyenBay import app, login, otp, mail, endpoint_secret
from flask import render_template, request, redirect, url_for, session, jsonify, json, request
import dao
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from flask_mail import *
import pdb

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from QLChuyenBay.models import Customer
#from QLChuyenBay.dao import remain_ticket
from models import UserRole

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html')

@app.route("/")
def home():
    airport_list = dao.get_air_port_list()
    return render_template("index.html", airport_list= airport_list)

@app.route('/verify', methods=["post", "get"])
def user_verify():
    err_msg = ''
    if request.method.__eq__("POST"):
        email = request.form.get('email')
        if email:
            check= dao.check_mail_exit(email=email)
            if check:
                session['email']=email
                msg = Message(subject='OTP', sender='anhqui04062004@gmail.com', recipients=[email])
                msg.body = str(otp)
                mail.send(msg)
                return redirect(url_for('user_validate'))
            else:
                err_msg= 'Email không tồn tại!!!'
    return render_template('verify.html', err_msg=err_msg)


@app.route('/validate', methods=["post", "get"])
def user_validate():
    if request.method.__eq__("POST"):
        user_otp = request.form.get('otp')
        if otp == int(user_otp):
            return render_template('reset_password.html')
    return render_template("otp.html", msg='Thất bại!!!')

@app.route('/reset-password', methods=['get', 'post'])
def reset_pwd():
    err_msg=''
    if request.method.__eq__("POST"):
        password= request.form.get("password")
        confirm= request.form.get("confirm")
        if not password.strip().__eq__(confirm.strip()):
            err_msg="Mật khẩu không khớp"
        else:
            dao.override_password(email= session.get('email'), password=password)

            return redirect(url_for('user_login'))
    return render_template('verify.html', err_msg=err_msg)

@app.route("/register", methods=['get', 'post'])
def user_register():
    err_msg = ''
    if request.method.__eq__("POST"):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            # if not dao.check_secure_password(password):
            #      err_msg='Mật khẩu chưa đủ mạnh'
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                dao.add_user(name=name, username=username, password=password,
                             email=email, avatar=avatar_path)
                return redirect(url_for('user_login'))
            else:
                err_msg = 'Mật khẩu không trùng khớp'
        except Exception as ex:
            err_msg = 'Hệ thống lỗi!!!'
    return render_template('register.html', err_msg=err_msg)

@app.route('/login-user', methods=['post', 'get'])
def user_login():
    err_msg = ''
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            next_page = request.args.get('next')
            if user.user_role.value == UserRole.ADMIN.value:
                return redirect('/admin')
            if user.user_role.value == UserRole.STAFF.value:
                return redirect('/admin')
            return redirect(next_page) if next_page else render_template('index.html')
        else:
            err_msg = "Username hoac password khong chinh xac!!!"
    return render_template('login.html', err_msg=err_msg)

@login_required
@app.route('/user-logout')
def user_logout():
    logout_user()
    session.clear()
    return redirect(url_for('user_login'))

@app.route('/api/admin-rule', methods=['post'])
def save_admin_rules():
    #data=request.get_json()
    min_time_flight = request.form.get('min-time-flight'),
    max_quantity_between_airport = request.form.get('max_quantity_between_airport'),
    min_time_stay_airport = request.form.get('min_time_stay_airport'),
    max_time_stay_airport = request.form.get('max_time_stay_airport'),
    time_book_ticket = request.form.get('time_book_ticket'),
    time_buy_ticket = request.form.get('time_buy_ticket')
    sa= dao.save_admin_rules(min_time_flight= min_time_flight,
                             max_quantity_between_airport= max_quantity_between_airport,
                             min_time_stay_airport= min_time_stay_airport,
                             max_time_stay_airport= max_time_stay_airport,
                             time_book_ticket= time_book_ticket,
                             time_buy_ticket= time_buy_ticket)
    if not sa:
        return {
            'status': 500,
            'data': 'error'
        }
    return {
        'status': 200,
        'data': 'success'
    }


@app.route('/api/admin-route-flight', methods=['post'])
def save_route_flight():
    data= request.json
    departure_airport= data.get('depart_airport')
    arrival_airport= data.get('arrival_airport')

    if departure_airport and arrival_airport:
        route_exists= dao.check_route_exists(departure_airport_id= dao.get_id_by_name_airport(departure_airport),
                                        arrival_airport_id= dao.get_id_by_name_airport(arrival_airport))
        if not route_exists:
            fr= dao.add_route_flight(departure_airport_id= dao.get_id_by_name_airport(departure_airport),
                                            arrival_airport_id= dao.get_id_by_name_airport(arrival_airport))
            return {
                'status': 200,
                'data': 'success'
            }
    return {
        'status': 500,
        'data': 'error'
    }

@app.route('/api/delete-route/<route_id>', methods=['delete'])
def delete_route(route_id):
    del_route= dao.del_route_id(route_id= route_id)
    if del_route:
        return {
            'status': 200,
            'data': 'success'
        }
    return {
        'status': 500,
        'data': 'error'
    }

@app.route('/api/flight-schedule', methods=['post'])
def create_flight_schedule():
    data = request.json
    depart_airport= data.get('depart_airport')
    arrival_airport= data.get('arrival_airport')
    time_start= data.get('time_start')
    time_end= data.get('time_end')
    quantity_1st_ticket= data.get('quantity_1st_ticket')
    quantity_2nd_ticket= data.get('quantity_2nd_ticket')
    price_type_1= data.get('price_type_1')
    price_type_2= data.get('price_type_2')
    airport_between_list= data.get('airportBetweenList')
    try:
        f = dao.create_flight_sche(depart_airport=depart_airport,
                                   arrival_airport=arrival_airport,
                                   time_start=time_start,
                                   time_end=time_end,
                                   quantity_1st_ticket=quantity_1st_ticket,
                                   quantity_2nd_ticket=quantity_2nd_ticket,
                                   price_type_1= price_type_1,
                                   price_type_2= price_type_2)
        for i in airport_between_list:
            bwa= dao.create_between_airport(airport_id=int(i['ap_id']),
                                            flight_sche_id=int(f.id),
                                            time_stay=float(i['ap_stay']),
                                            note=i['ap_note'])
    except Exception as err:
        return {
            'status': 500,
            'data': err
        }
    return {
        'status': 200,
        'data': 'success'
    }

@app.route('/api/flight-schedule/details-schedule', methods=['post'])
def get_data_details_schedule():
    data= request.json

    details= dao.get_flight_sche_json(request.json.get('flight_schedule_id'))
    if details:
        return {
            'data': 'success',
            'status': 200
        }
    return {

        'data': 'err',
        'status': 500
    }

@app.route('/api/flight_schedule/search', methods=['post'])
def search_flight_schedule():
    data = request.json
    departure_airport_id= data.get('departure_airport_id')
    departure_airport_name= data.get('departure_airport_name').strip()
    arrival_airport_id= data.get('arrival_airport_id')
    arrival_airport_name= data.get('arrival_airport_name').strip()
    time_start= data.get('time_start')
    ticket_type= data.get('ticket_type')


    try:
        inp_search = dao.get_inp_search_json(departure_airport_id=departure_airport_id,
                                             departure_airport_name=departure_airport_name,
                                             arrival_airport_id=arrival_airport_id,
                                             arrival_airport_name=arrival_airport_name,
                                             time_start=time_start,
                                             ticket_type=ticket_type)

        data_search = dao.search_flight_sche(departure_airport_id= departure_airport_id,
                                             arrival_airport_id= arrival_airport_id,
                                             time_start=time_start,
                                             ticket_type=ticket_type)

        session['data_search'] = data_search
        session['inp_search'] = inp_search

    except Exception as error:
        return {
            'status': 500,
            'data': error
        }
    return {
        'status': 200,
        'data': data_search
    }

@app.route('/flight-list')
def flight_list():
    admin_rules= dao.get_rule_admin()

    return render_template('flightList.html', admin_rules= admin_rules)

@app.route('/ticket/<int:flight_id>')
def get_ticket(flight_id):
    ticket_type= request.args.get('ticket-type')
    f = dao.get_flight_sche_json(flight_id)
    # user_id= current_user.get_id()
    # data_customers= session['ticket']['customers_info'][0]['data']
    # quantity_customers= session['ticket']['customers_info'][0]['quantity']
    #
    # name_customer= []
    # for name in range(0, quantity_customers):
    #     name_customer.append(data_customers[name]['name'])
    # ticket_id= dao.get_list_id_ticket(session['ticket']['f_id'], name_customer, user_id)
    seat_active= dao.get_seat_number_active(flight_id)
    return render_template('ticket.html',ticket_type=ticket_type, f=f,
                           user_role=UserRole, seat_active= seat_active)

@app.route('/bill_ticket/<int:f_id>')
def bill_ticket(f_id):
    user_id = current_user.get_id()
    flight_id = session['ticket']['f_id']
    package_price = session['ticket']['package_price']
    ticket_type = session['ticket']['ticket_type']
    ticket_price = (int(session['ticket']['total']) - int(package_price))
    for d in range(len(session['ticket']['customers_info'][0]['data'])):
        cr = dao.create_ticket(user_id=user_id, flight_id=flight_id,
                               customer_id=session['ticket']['customers_info'][0]['data'][d]['id'],
                               ticket_price=ticket_price,
                               ticket_type=ticket_type, package_price=package_price,
                               customer_email=session['ticket']['customers_info'][0]['data'][d]['id_customer'],
                               customer_phone=session['ticket']['customers_info'][0]['data'][d]['phone'],
                               customer_name=session['ticket']['customers_info'][0]['data'][d]['name'],
                               seat_number=session['ticket']['customers_info'][0]['data'][d]['seat_number'])

    if current_user.user_role.value == UserRole.USER.value:
        email = dao.get_email_by_user(user_id)
        msg = Message(subject='Thông báo về việc thanh toán vé máy bay PhuQuiAirFlight',
                      sender='anhqui04062004@gmail.com', recipients=[email])
        msg.body = ('Bạn đã thanh toán thành công: ' + str(session['ticket']['total']) +
                    ' VND. Chúc bạn có một chuyến đi tốt lành')
        mail.send(msg)
    ticket_list_json=dao.get_ticket_list_json(user_id= user_id)
    return render_template('billTicket.html', ticket_list_json= ticket_list_json)


@app.route('/api/ticket/<int:f_id>', methods=['post'])
def create_ticket(f_id):
    data= request.json
    id = data.get('f_id')
    type_ticket= data.get('ticket_type')
    session['ticket']= data

    remain_ticket=dao.get_ticket_remain(id, type_ticket)

    if remain_ticket < data['customers_info'][0]['quantity']:
        return {
            'status': 500,
            'data': "Chỉ có thể đặt tối đa %s vé!" % remain_ticket
        }
    # if data['user_role'] == 'UserRole.STAFF' or data['user_role'] == 'UserRole.ADMIN':
    #     check_time = dao.check_time_ticket(id, is_user=False)
    #     if not check_time['state']:
    #         return {
    #             'status': 500,
    #             'data': "Không thể đặt vé cách giờ bay trước %s tiếng!" % check_time['min']
    #         }
    #     # pay_ticket(data['f_id'], is_staff=True)
    # else:
    # check_time = dao.check_time_ticket(id)
    # import pdb
    # pdb.set_trace()
    # if not check_time['state']:
    #     return {
    #         'status': 500,
    #         'data': "Không thể đặt vé cách giờ bay trước %s tiếng!" % check_time['min']
    #     }
    return {
        'status': 200,
        'data': data['f_id']
    }

@login_required
@app.route('/create-checkout-session/<int:f_id>', methods=['post'])
def create_checkout_session(f_id):
    try:
        checkout_session= stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'vnd',
                        'product_data': {
                            'name': 'PhuQuiAirFlight',
                        },
                        'unit_amount': int(session['ticket']['total']),
                    },
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url=app.config['MY_DOMAIN'] + '/bill_ticket/' + session['ticket']['f_id'],
            cancel_url= app.config['MY_DOMAIN'] + '/error'
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code= 303)


@app.route('/error')
def error():
    return 'error'

@login_required
@app.route('/list-flight-payment/<int:f_id>')
def list_flight_payment(f_id):
    quantity_customers= int(session['ticket']['customers_info'][0]['quantity'])
    data= session['ticket']['customers_info'][0]['data']
    quantity_ticket= dao.count_ticket()
    return render_template('listFlightChoose.html',
                           quantity_ticket= quantity_ticket, quantity_customers= quantity_customers, data= data)


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)

@app.context_processor
def common_attributes():
    return {
        'user_role': UserRole
    }

if __name__ == '__main__':
    from QLChuyenBay.admin import *
    app.run( debug=True, host='localhost', port=5002)
