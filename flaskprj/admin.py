from flask_admin.contrib import sqla
from flask_admin import AdminIndexView
from flask_login import current_user, login_required

class BlogModelView(sqla.ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated
        try:
            return current_user.is_accessible
        except:
            return False


class BlogAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            return current_user.is_accessible
        except:
            return False
    