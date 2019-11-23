
from pymongo import MongoClient
import pandas as pd

class MongoWrapper:
    def __init__(self):
        self._client = MongoClient(host=['localhost:27017'])
        print('Mongo initiation: OK')

    def query(self, names, categories, gt, min_rating, orderby, sortRule, stats, columns):

        # Access database
        apps = self._client['test']['apps']

        condition = "$gt"
        if gt == -1:
            condition = "$lt"

        filters = {}

        if len(names) and len(categories) and gt:
            filters = {
                "name" : { "$in" : names },
                "categories" : { "$in" : categories },
                "rating" : { condition : min_rating }
            }
        else:
            if len(names) and len(categories):
                filters = {
                    "name" : { "$in" : names},
                    "categories" : { "$in" : categories }
                }
            else:
                if len(names) and gt:
                    filters = {
                        "name" : { "$in" : names },
                        "rating" : { condition : min_rating }
                    }
                else:
                    if len(categories) and gt:
                        filters = {
                            "categories" : { "$in" : categories }
                        }
                    else:
                        if len(names):
                            filters = {
                                "name" : { "$in" : names }
                            }
                        else:
                            if len(categories):
                                filters = {
                                    "categories" : { "$in" : categories }
                                }
                            else:
                                if gt:
                                    filters = {
                                        "rating" : { condition : min_rating }
                                    }


        statistics = {}
        results = apps.find(filters)

        if orderby:
            print('TO DO...')
#            results = results.sort_values(by=[orderby], ascending = (sort == sortRule))

        results = list(results)

        if 'amounts' in stats:
            apple = 0
            google = 0
            shopify = 0

            for i in results:
                words = str(i).split()

                print('\n\n', flush = True)
                for word in words:
                    print(word, flush = True)
                    if word == '\'apple_apps\':':
                        apple = apple + 1
                    if word == '\'google_apps\':':
                        google = google + 1
                    if word == '\'shopify_apps\':':
                        shopify = shopify + 1

            statistics['amounts'] = 'Apple Store has ' + str(apple) + ' apps. Google Store has ' + str(google) + ' apps. Shopify Store has ' + str(shopify) + ' apps.'
        else:
            statistics['amounts'] = ''

        if 'categories' in stats:
            print("TO DO...")
        else:
            statistics['categories'] = ''

        if 'prices' in stats:
            print("TO DO...")
        else:
            statistics['prices'] = ''

#        return results[columns], statistics if len(columns) else results, statistics
        return [], []
