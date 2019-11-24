
from pymongo import MongoClient
import pandas as pd
import numpy as np
import re

class MongoWrapper:
    def __init__(self):
            self._client = MongoClient(host=['localhost:27017'])
            print('Mongo initiation: OK')

    def query(self, names, categories, gt, min_rating, orderBy, sortRule, required_stats, reviews):
        ###################################################################################
        # Initiation
        ###################################################################################

        # Access database
        apps = self._client['test']['apps']

        # Conditions
        where      = {}
        projection = {'_id' : 0}
        projection['id'] = 1
        columns = ['id']

        # Projection
        if not reviews:
            projection['name'] = 1
            projection['categories'] = 1
            projection['apps_price_plans'] = 1
            projection['rating'] = 1
            projection['age_rating'] = 1
            projection['apple_apps']   = 1
            projection['google_apps']  = 1
            projection['shopify_apps'] = 1

            columns.append('name')
            columns.append('categories')
            columns.append('apps_price_plans')
            columns.append('rating')
            columns.append('age_rating')
            columns.append('apple_apps')
            columns.append('google_apps')
            columns.append('shopify_apps')

        if 'amounts' in required_stats:
            projection['apple_apps']   = 1
            projection['google_apps']  = 1
            projection['shopify_apps'] = 1

            if 'apple_apps' not in columns:
                columns.append('apple_apps')
                columns.append('google_apps')
                columns.append('shopify_apps')

        if 'categories' in required_stats:
            projection['categories'] = 1

            if 'categories' not in columns:
                columns.append('categories')

        if 'prices' in required_stats:
            projection['apps_price_plans'] = 1

            if 'apps_price_plans' not in columns:
                columns.append('apps_price_plans')

        #----------------------------------------------------------------------------------
        # Build where conditions
        #----------------------------------------------------------------------------------

        if names:
            where['name'] = { '$in' : names }

        if categories:
            where['categories'] = { '$in' : categories }

        #----------------------------------------------------------------------------------
        # Do the query
        #----------------------------------------------------------------------------------

        results = apps.find(where, projection)

        ###################################################################################
        # Initial return values
        ###################################################################################

        table = pd.DataFrame(columns = columns)
        stats = {
            'amounts' : {
                'apple' : 0,
                'google' : 0,
                'shopify' : 0,
            },
            'categories' : [],
            'prices' : {
                'sum' : 0.0,
                'count' : 0,
                'min' : float("inf"),
                'max' : 0.0
            }
        }

        ###################################################################################
        # Builds the return values
        ###################################################################################

        counter = 0
        for doc in results:

            fRating = 0.0
            strRating = str(int(doc['rating']))
            if len(strRating) == 1:
                fRating = float(strRating + '.0')
            else:
                fRating = float(strRating[0] + '.' + strRating[1])

            if (gt == 1 and fRating <= min_rating) or (gt == -1 and fRating >= min_rating):
                continue

            #----------------------------------------------------------------------------------
            # Builds app information
            #----------------------------------------------------------------------------------
            row = []

            for c in columns:

                if c in doc:
                    if c == 'id':
                        row.append(str(int(doc[c])))
                    elif c == 'rating':
                        row.append(fRating)
                    else:
                        if c != 'apple_apps' and c != 'google_apps' and c != 'shopify_apps':
                            row.append(re.sub('[^A-Za-z0-9 ,:.]+', '', str(doc[c])))
                        else:
                            row.append(str(doc[c]))

                # Error: column must be in the projection
                else:
                    row.append(np.NaN)

            counter += 1
            if counter > 50:
                break

            # Build a new row of the table
            table.loc[0 if table.empty else table.index.max() + 1] = row

            #----------------------------------------------------------------------------------
            # Builds app stats
            #----------------------------------------------------------------------------------

            if 'amounts' in required_stats:
                if 'apple_apps' in doc:
                    stats['amounts']['apple'] += 1
                if 'google_apps' in doc:
                    stats['amounts']['google'] += 1
                if 'shopify_apps' in doc:
                    stats['amounts']['shopify'] += 1

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

        ###################################################################################
        # Final verification
        ###################################################################################

        if orderBy:
            table = table.sort_values(by=orderBy, ascending=sortRule, na_position='first')

        #----------------------------------------------------------------------------------
        # Builds app stats
        #----------------------------------------------------------------------------------

        return table, stats
