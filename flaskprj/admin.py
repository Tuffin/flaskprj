from flask_admin.contrib import sqla
from flask_admin import AdminIndexView
from flask_login import current_user

class BlogModelView(sqla.ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.is_accessible


class BlogAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_accessible
    