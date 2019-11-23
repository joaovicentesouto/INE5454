
from pymongo import MongoClient
import pandas as pd

class MongoWrapper:
    def __init__(self):
        self._client = MongoClient(host=['localhost:27017'])
        print('Mongo initiation: OK')

    def query(self, names, categories, gt, min_rating, orderby, sortRule, stats, filters = []):

        ratingValue = min_rating
        condition = '$gt'

        if gt == -1:
            condition = '$lt'

        if gt == 0:
            ratingValue = 0

        # Access database
        apps = self._client['database']['apps']

        q = {
            'name' : { '$in' : names },
            'categories' : { '$in' : categories },
            'rating' : { condition : ratingValue },
        }

#        result = list(apps.find(q))
        result = apps.find(q)
        print(result)

#        if 'amount' is in stats:
#            for i, j in result:
#                if

#        if orderby:
#            result = result.sort_values(by = [orderby], ascending = (sort == sortRule))

        return result, []#result[filters] if len(filters) else result, [amount, categories, prices]
