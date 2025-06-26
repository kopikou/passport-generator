import traceback

from mssql import features, base

class DatabaseFeatures(features.DatabaseFeatures):
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False

class DatabaseWrapper(base.DatabaseWrapper):
    _sql_server_versions = {**base.DatabaseWrapper._sql_server_versions, 8: 2000}
    features_class = DatabaseFeatures

    def _close(self):
        if self.connection is not None:
            with self.wrap_database_errors:
                try:
                    self.connection.commit()
                except Exception as ex:
                    traceback.print_stack()
                return self.connection.close()