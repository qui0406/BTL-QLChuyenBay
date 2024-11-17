import math
from QLChuyenBay import app, login
from flask import render_template, request, redirect, url_for, session, jsonify
import dao
import cloudinary.uploader
from flask_login import login_user, logout_user

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['get', 'post'])
def user_register():
    err_msg=''
    if request.method.__eq__("POST"):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        avatar_path= None

        try:
            # if not dao.check_secure_password(password):
            #      err_msg='Mật khẩu chưa đủ mạnh'
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                dao.add_user(name= name, username= username, password= password,
                             email= email, avatar= avatar_path)
                return redirect(url_for('user_login'))
            else:
                err_msg= 'Mật khẩu không trùng khớp'
        except Exception as ex:
            err_msg= 'Hệ thống lỗi!!!'
    return render_template('register.html', err_msg= err_msg)

@app.route('/login-user', methods=['post', 'get'])
def user_login():
    err_msg=''
    if request.method.__eq__("POST"):
        username= request.form.get('username')
        password= request.form.get('password')
        user= dao.check_login(username= username, password= password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = "Username hoac password khong chinh xac!!!"
    return render_template('login.html', err_msg= err_msg)

@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id= user_id)

if __name__=='__main__':
    app.run(debug=True)