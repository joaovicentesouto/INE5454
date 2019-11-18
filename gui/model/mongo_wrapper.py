# import pymongo requires pip3 install pymongo

from pymongo import MongoClient

class MongoWrapper:

	def __init__(self):
		self._client = MongoClient(host=['localhost:27017'])
		print('Mongo initiation: OK')

	def query(self, categories, stores = [], min_rating = 0, sort = 'desc', filters = []):

		# Access database
		apps = self._client['database']['apps']

		q = {
			'categories' : { '$in' : categories },
			'rating' : { '$gt' : min_rating }
		}

		if stores:
			q['$or'] = []
			for s in stores:
				q['$or'].append({s : { '$exists' : 1 }})
		
		f = {'_id' : 0}

		if filters:
			for i in filters:
				f[i] = 1

		# Query
		result = apps.find(q, f)

		return list(result)
