from kingadmin.admin_base import AdminBase

class Recoder(object):
    def __init__(self):
        self.enble_admin={}
        self.model=None
    def register(self,class_model,class_admin=None):
        app_name=class_model._meta.app_label
        model_name=class_model._meta.model_name

        if not class_admin:
            class_admin=AdminBase

        class_admin.model=class_model

        if app_name not in self.enble_admin:
            self.enble_admin[app_name]={}
        self.enble_admin[app_name][model_name]=class_admin

site=Recoder()