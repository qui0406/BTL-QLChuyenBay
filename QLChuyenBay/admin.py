from QLChuyenBay import app, db
from flask_admin import Admin, expose, AdminIndexView
from QLChuyenBay.models import  User, AirPort
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_login import current_user, logout_user
from flask import redirect
import dao

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__('ADMIN')


class AuthenticatedStaff(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__('STAFF')

class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(MyView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class RulesView(MyView):
    @expose('/')
    def index(self):
        admin_rules= dao.get_rule_admin()
        return self.render('admin/rules.html', admin_rules=admin_rules)

class StatsView(MyView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


admin= Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4', index_view= MyAdminIndex())
admin.add_view(AuthenticatedAdmin(User, db.session))
admin.add_view(AuthenticatedAdmin(AirPort, db.session))
# admin.add_view(AuthenticatedAdmin(FlightRoute, db.session))

admin.add_view(RulesView(name='Quản lý quy định'))
admin.add_view(StatsView(name= 'Thống kê'))
admin.add_view(LogoutView(name= 'Logout'))