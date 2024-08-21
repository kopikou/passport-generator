class MainRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'arim':
            return 'mira'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'arim':
            return 'mira'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'arim' \
                or obj2._meta.app_label == 'arim':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'mira' or app_label == 'arim':
            return False
        return None


class LibraryRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'arim_library':
            return 'mira_library'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'arim_library':
            return 'mira_library'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'arim_library' \
                or obj2._meta.app_label == 'arim_library':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'mira_library' or app_label == 'arim_library':
            return False
        return None

class RpdRouter(object):
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'rpd_old':
            return False
        return None