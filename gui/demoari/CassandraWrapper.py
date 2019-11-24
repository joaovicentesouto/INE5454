# import cassandra requires pip3 install cassandra-driver

from cassandra.cluster import Cluster
import pandas as pd

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

class CassandraWrapper:
    def __init__(self):
        self._client = Cluster(['localhost'], port=9042)
        print('Cassandra initiation: OK')

    def query(self, ids, orderby, sortRule, sentiment):

            session = self._client.connect(keyspace='test')

            # Defines format of the result
            session.row_factory = pandas_factory
            session.default_fetch_size = None

            # Builds WHERE argument
            ids = ', '.join(list(map(str, ids)))

            print(ids, flush = True)

            # Performs the query
            rows = session.execute('SELECT * FROM test.reviews WHERE app_id IN (%s) ALLOW FILTERING' % (ids))

            table = rows._current_rows

            if orderby:
                table = table.sort_values(by=orderBy, ascending=sortRule, na_position='last')

            return table
