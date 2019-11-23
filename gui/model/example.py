from mongo_wrapper import MongoWrapper
from cassandra_wrapper import CassandraWrapper

m = MongoWrapper()
res_m = m.query(categories = ['games'], stores = ['apple_apps', 'shopify_apps'], min_rating = 10, sort = 'asc', filters = ['id', 'categories', 'name'])
print(res_m)

c = CassandraWrapper()

# Listagem dos reviews de um ou mais aplicativo
# res_c = c.query(ids = [1188432952, 1188375927], columns = ['app_id', 'content'])

# Listagem dos comentários com rating baixo (ou alto) de um ou mais aplicativos
# res_c = c.query(ids = [1188432952, 1188375927], columns = ['app_id', 'content', 'rating'], orderby = 'rating', sort = 'asc')

# Listagem dos comentários com sentimento mais negativo (ou positivo) de um ou mais aplicativos
res_c = c.query(ids = [1188432952, 1188375927], columns = ['app_id', 'content', 'sentiment_polarity'], orderby = 'sentiment_polarity', sort = 'desc')

print(res_c)

