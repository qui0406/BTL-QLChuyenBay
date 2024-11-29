import math
import pdb
from logging import error

from QLChuyenBay import app, login, otp, mail
from flask import render_template, request, redirect, url_for, session, jsonify
import dao
import cloudinary.uploader
from flask_login import login_user, logout_user
from flask_mail import *
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
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = "Username hoac password khong chinh xac!!!"
    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def signin_admin():
    username= request.form.get('username')
    password = request.form.get('password')
    user = dao.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')

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

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from QLChuyenBay.admin import *
    app.run(debug=True, host='localhost', port=5002)
