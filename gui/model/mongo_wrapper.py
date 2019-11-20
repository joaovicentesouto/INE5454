# import pymongo requires pip3 install pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np

class MongoWrapper:

	def __init__(self):
		self._client = MongoClient(host=['localhost:27017'])
		print('Mongo initiation: OK')

	def query(self, categories, stores = [], min_rating = 0, sort = 'desc', filters = [], required_stats = []):

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

		if 'amount' in required_stats:
			f['apple_apps'] = 1
			f['google_apps'] = 1
			f['shopify_apps'] = 1

		if 'categories' in required_stats:
			f['categories'] = 1

		if 'prices' in required_stats:
			f['apps_price_plans'] = 1

		# Query
		results = apps.find(q, f)

		df = pd.DataFrame(columns=filters)
		stats = {
			'amounts' : {
				'apple' : 0,
				'google' : 0,
				'shopity' : 0,
			},
			'categories' : [],
			'prices' : {
				'sum' : 0.0,
				'count' : 0,
				'min' : float("inf"),
				'max' : 0.0
			}
		}

		for doc in results:

			# Builds app information
			row = []

			for f in filters:
				if f in doc:
					if isinstance(doc[f], list):
						row.append(', '.join(doc[f]))
					elif isinstance(doc[f], dict):
						row.append(str(doc[f]))
					else:
						row.append(doc[f])
				else:
					row.append(np.NaN)

			df.loc[0 if df.empty else df.index.max() + 1] = row

			# Builds app stats
			if 'amounts' in required_stats:
				if 'apple_apps' in doc:
					stats['amounts']['apple'] += 1
				if 'google_apps' in doc:
					stats['amounts']['google'] += 1
				if 'shopity_apps' in doc:
					stats['amounts']['shopity'] += 1

			if 'categories' in required_stats:
				for cat in doc['categories']:
					if cat not in categories:
						stats['categories'].append(cat)

			if 'prices' in required_stats:
				for plan in doc['apps_price_plans']:
					for currency in plan['currencies']:
						stats['prices']['sum'] += currency['price']
						stats['prices']['count'] += 1

						if currency['price'] < stats['prices']['min']:
							stats['prices']['min'] = currency['price']

						if currency['price'] > stats['prices']['max']:
							stats['prices']['max'] = currency['price']

		return df, stats
