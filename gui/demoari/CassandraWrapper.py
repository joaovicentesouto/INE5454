# import cassandra requires pip3 install cassandra-driver

from cassandra.cluster import Cluster
import pandas as pd

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

class CassandraWrapper:
    def __init__(self):
        self._client = Cluster(['localhost'], port=9042)
        print('Cassandra initiation: OK')

    def query(self, ids, orderBy, sortRule, sentiment, sentimentType, polarity, polarityValue):

        ###################################################################################
        # Initiation
        ###################################################################################

        session = self._client.connect(keyspace='test')

        #----------------------------------------------------------------------------------
        # Build where conditions
        #----------------------------------------------------------------------------------

        # Defines format of the result
        session.row_factory = pandas_factory
        session.default_fetch_size = None

        columns = '\
            app_id, \
            author, \
            content, \
            developer_reply, \
            developer_reply_post_date, \
            helpful_count, \
            post_date, \
            rating, \
            sentiment_type, \
            sentiment_polarity, \
            sentiment_subjectivity'

        connector = ''

        where = ''
        if sentiment:
            where = 'sentiment_type IN (\'' + sentimentType + '\')'
            connector = ' AND '

        if polarity:
            if polarity < 0:
                where = where + connector + 'sentiment_polarity < ' + str(polarityValue)
            else:
                where = where + connector + 'sentiment_polarity > ' + str(polarityValue)
            connector = ' AND '

        if not polarity and orderBy:
            where = where + connector + 'sentiment_polarity >= -1 AND sentiment_polarity <= 1'
            connector = ' AND '

        #----------------------------------------------------------------------------------
        # Do the query
        #----------------------------------------------------------------------------------

        # Performs the query

        table = pd.DataFrame()

        for id in ids:
            print('SELECT ' + columns + ' FROM test.reviews WHERE ' + where + connector + 'app_id IN (' + id + ') ALLOW FILTERING', flush = True)
            rows = session.execute('SELECT ' + columns + ' FROM test.reviews WHERE ' + where + connector + 'app_id IN (' + id + ') ALLOW FILTERING')
            table = pd.concat([table, rows._current_rows], ignore_index = True)
            if table.shape[0] > 1000:
                break

        ###################################################################################
        # Gets table result (pandas dataframe)
        ###################################################################################

        if orderBy and orderBy == 'sentiment_polarity':
            table = table.sort_values(by=orderBy, ascending=sortRule, na_position='last')

        return table
