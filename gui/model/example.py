from mongo_wrapper import MongoWrapper
from cassandra_wrapper import CassandraWrapper

m = MongoWrapper()
res_m = m.query(categories = ['games'], stores = ['apple_apps', 'shopify_apps'], min_rating = 10, sort = 'asc', filters = ['id', 'categories', 'name'])
print(res_m)

c = CassandraWrapper()
res_c = c.query(ids = [1188432952], columns = ['app_id', 'content', 'rating'], orderby = 'rating', sort = 'desc')
print(res_c)
