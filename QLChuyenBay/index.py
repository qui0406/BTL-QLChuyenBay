from QLChuyenBay import app, login, otp, mail
from flask import render_template, request, redirect, url_for, session, jsonify
import dao
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from flask_mail import *
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from models import UserRole

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html')

@app.route("/")
def home():
    return render_template("index.html")

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
            if user.user_role.value == UserRole.ADMIN.value:
                return redirect('/admin')
            if user.user_role.value == UserRole.STAFF.value:
                return redirect('/admin')
            return render_template('index.html')
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
   # data=request.get_json()
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
    departure_airport= request.form.get('departure')
    arrival_airport= request.form.get('arrival')
    if departure_airport and arrival_airport:
        fr= dao.change_airport_to_id(departure_airport, arrival_airport)
        if fr:
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

@app.route('/api/flight-schedule', methods=['POST'])
def create_flight_schedule():

    depart_airport= int(request.form.get('departure_airport_sche').split(".")[0])
    arrival_airport= int(request.form.get('arrival_airport_sche').split(".")[0])
    time_start= request.form.get('time_start')
    time_end= request.form.get('time_end')
    quantity_1st_ticket= int(request.form.get('quantity_1st_ticket'))
    quantity_2nd_ticket= int(request.form.get('quantity_2nd_ticket'))
    price_type_1= float(request.form.get('price_type_1'))
    price_type_2= float(request.form.get('price_type_2'))

    try:
        f = dao.create_flight_sche(depart_airport=depart_airport,
                                   arrival_airport=arrival_airport,
                                   time_start=time_start,
                                   time_end=time_end,
                                   quantity_1st_ticket=quantity_1st_ticket,
                                   quantity_2nd_ticket=quantity_2nd_ticket,
                                   price_type_1= price_type_1,
                                   price_type_2= price_type_2)

        # for a in data['airportBetweenList']:
        #     bwa= dao.create_between_airport(airport_id=a['ap_id'], flight_sche_id=f.id, time_stay=a['ap_stay'],
        #                              note=a['ap_note'])
        #     test = dao.get_flight_sche_list()

    except Exception as err:
        return {
            'status': 500,
            'data': err
        }
    return {
        'status': 200,
        'data': 'success'
    }

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
    app.run(debug=True, host='localhost', port=5002)
