class RPDRouter(object):
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'rpd_old':
            return False
        return None