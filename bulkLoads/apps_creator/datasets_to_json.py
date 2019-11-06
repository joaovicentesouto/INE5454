#mymodule.py

### BEGIN ### Mapping from Apple dataset to json structure
'''

{
    "id": <id>,
    "categories": [{"name": <prime_genre>}], (Remember to break the composed genres)
    "apps_price_plans": [{"currencies:" [{"currency": <currency>,"price": <price>}]}],
    "age_rating": <cont_rating>,
    "name": <track_name>, (Verify if this name already exists in Google or Shopify stores)
    "rating": <user_rating>,
    "apple_apps":
    {
        "app_description": <app_description>, (Get from appleStore_description.csv by app id)
        "version": <ver>,
        "n_of_supported_devices":<sup_devices>,
        "n_of_reviews": <rating_count_tot>,
        "n_of_ipad_urls": <ipadSc_urls>,
        "n_of_available_languages": <lang>,
        "belongs_to_volume_purchase_program": <vpp_lic>,
        "rating_curr_version": <user_rating_ver>,
        "n_of_rating_curr_version": <rating_count_ver>,
        "size": <size_bytes>
    }
}


'''
### END ###


### BEGIN ### Mapping from Google dataset to json structure
'''

{
	"id": <id>, (Generate the Google app ids with the Joao formule)
	"categories": [{"name": <Category>},{"name": <Genres>}], (Remember to break the composed genres and categories)
	"apps_price_plans": [{"name": <Type>, "currencies": [{"price": <Price>}]}],
	"age_rating": <Content Rating>, (Remember to create a value accordingly to age rating category)
	"name": <App>, (Verify if this name already exists in Shopify store)
	"rating": <Rating>,
	"google_apps":
	{
		"version": <Current Ver>,
		"size": <Size>, (Convert from Megabytes to bytes)
		"n_of_reviews": <Reviews>,
		"android_version_required": <Android Ver>,
		"latest_update_at_store": <Last Updated>,
		"n_of_downloads": <Installs>
	}
}

'''
### END ###


### BEGIN ### Mapping from Shopify dataset to json structure
'''

{
	"id": <id>, (Verify if this id already exists and get the greatest id in the dataset plus one)
	"categories": [{"name": <title>}], (Get the id attribute from apps file; get all category_id on apps_categories that is attached to app id; get the corresponding category name for the obtained category ids on categories file)
	"apps_price_plans": [{"name": <title>, (Get the id attribute from apps file; get the corresponding plan name from pricing_plans file)
						  "feature": <feature>, (Get the id attribute from apps file; get the corresponding plan feature from pricing_plan_feature file)
						  "currencies": [{"currency": <price>, (Get the id attribute from apps file; get the corresponding currency from pricing_plans file. Ignore the price)
						  				  "price": <price>}]}] (Get the id attribute from apps file; get the corresponding price from pricing_plans file. Ignore the price currency and period; convert strings to values)
	"name": <title>,
	"rating": <rating>,
	"shopify_apps":
	{
			"developer": {"name": <developer>, "link": <developer_link>}
            "app_description": <description>,
            "app_raw_description": <description_raw>,
            "url": <url>,
            "tagline": <tagline>,
            "icon": <icon>,
            "benefit_name": <title>, (Get the id attribute from apps file; get the corresponding benefit name from key_benefits file)
            "benefit_description": <description>, (Get the id attribute from apps file; get the corresponding benefit description from key_benefits file)
            "free_trial_days": <pricing_hint>,
            "n_of_reviews": <reviews_count>
	}
}

'''
### END ###


### BEGIN ### Import libraries to manipulate the csv files

import pandas as pd
import os

### END ###


### BEGIN ### Definition of all files used in this script

apple_file1 = '../../datasets/Apple/AppleStore.csv'
apple_file2 = '../../datasets/Apple/appleStore_description.csv'

google_file1 = '../../datasets/Google/googleplaystore.csv'

shopify_file1 = '../../datasets/Shopify/apps.csv'
shopify_file2 = '../../datasets/Shopify/apps_categories.csv'
shopify_file3 = '../../datasets/Shopify/categories.csv'
shopify_file4 = '../../datasets/Shopify/key_benefits.csv'
shopify_file5 = '../../datasets/Shopify/pricing_plan_features.csv'
shopify_file6 = '../../datasets/Shopify/pricing_plans.csv'

script_file = './MongoDB_bulkLoad.js'

### END ###




Size
Installs
Type
Price
Content Rating
Genres
Last Updated
Current Ver
Android Ver






### BEGIN ### Tries to open all necessary datasets

try:

	apple_f1_df = pd.read_csv(apple_file1, sep=',', quotechar='"', encoding='utf8')

	apple_f1_df['id']     			= apple_f1_df['id'].map(lambda x : x.lower())
	apple_f1_df['track_name'] 		= apple_f1_df['track_name'].map(lambda x : x.lower())
	apple_f1_df['size_bytes']   	= apple_f1_df['size_bytes'].map(lambda x : x.lower())
	apple_f1_df['currency'] 	 	= apple_f1_df['currency'].map(lambda x : x.lower())
	apple_f1_df['price']   			= apple_f1_df['price'].map(lambda x : x.lower())
	apple_f1_df['rating_count_tot']	= apple_f1_df['rating_count_tot'].map(lambda x : x.lower())
	apple_f1_df['rating_count_ver']	= apple_f1_df['rating_count_ver'].map(lambda x : x.lower())
	apple_f1_df['user_rating']   	= apple_f1_df['user_rating'].map(lambda x : x.lower())
	apple_f1_df['user_rating_ver']  = apple_f1_df['user_rating_ver'].map(lambda x : x.lower())
	apple_f1_df['ver']   			= apple_f1_df['ver'].map(lambda x : x.lower())
	apple_f1_df['cont_rating']   	= apple_f1_df['cont_rating'].map(lambda x : x.lower())
	apple_f1_df['prime_genre']   	= apple_f1_df['prime_genre'].map(lambda x : x.lower())
	apple_f1_df['sup_devices.num']  = apple_f1_df['sup_devices'].map(lambda x : x.lower())
	apple_f1_df['ipadSc_urls.num']  = apple_f1_df['ipadSc_urls'].map(lambda x : x.lower())
	apple_f1_df['lang.num']   		= apple_f1_df['lang'].map(lambda x : x.lower())
	apple_f1_df['vpp_lic']   		= apple_f1_df['vpp_lic'].map(lambda x : x.lower())

	apple_f2_df = pd.read_csv(apple_file2, sep=',', quotechar='"', encoding='utf8')

	apple_f2_df['id']   		= apple_f2_df['id'].map(lambda x : x.lower())
	apple_f2_df['track_name']   = apple_f2_df['track_name'].map(lambda x : x.lower())
	apple_f2_df['size_bytes']   = apple_f2_df['size_bytes'].map(lambda x : x.lower())
	apple_f2_df['app_desc']   	= apple_f2_df['app_desc'].map(lambda x : x.lower())

	google_f1_df = pd.read_csv(google_file1, sep=',', quotechar='"', encoding='utf8')

	apple_f2_df['app_desc']   	= apple_f2_df['app_desc'].map(lambda x : x.lower())

	shopify_f1_df = pd.read_csv(shopify_file1, sep=',', quotechar='"', encoding='utf8')
	shopify_f2_df = pd.read_csv(shopify_file2, sep=',', quotechar='"', encoding='utf8')
	shopify_f3_df = pd.read_csv(shopify_file3, sep=',', quotechar='"', encoding='utf8')
	shopify_f4_df = pd.read_csv(shopify_file4, sep=',', quotechar='"', encoding='utf8')
	shopify_f5_df = pd.read_csv(shopify_file5, sep=',', quotechar='"', encoding='utf8')
	shopify_f6_df = pd.read_csv(shopify_file6, sep=',', quotechar='"', encoding='utf8')

except IOError:

	print('Was not able to open some dataset. Please check!')
	exit(1)

### END ###


### BEGIN ### Auxiliar methods

def category_split(content, splitter):

	content_vector = content.split(splitter)

	categories = '{"name":' + content_vector[0] + '}'

	for i in range(1, len(content_vector)):
		categories = categories + ',{"name":' + content_vector[i] + '}'

	return categories

def get_from_another_file(file, column, value, attribute):

	try:

		row = file[file[column] == value].index

		return 1, file.loc[row, attribute][0]

	except Exception as e:

		return 0, ''

def get_vector_from_another_file(file, column, value, attribute):

	try:

		row = file[file[column] == value].index

		return 1, file.loc[row, attribute]

	except Exception as e:

		return 0, []


def look_app(app_name, store):

	if store == 0:

		global apple_f1_df
		global apple_f2_df

		try:

			row = apple_f1_df[apple_f1_df['track_name'] == app_name].index

			# Simple cases

			app_id = apple_f1_df.loc[row, 'id'][0]
			size_bytes = str(apple_f1_df.loc[row, 'size_bytes'][0])
			rating_count_tot = str(apple_f1_df.loc[row, 'rating_count_tot'][0])
			rating_count_ver = str(apple_f1_df.loc[row, 'rating_count_ver'][0])
			user_rating_ver = str(apple_f1_df.loc[row, 'user_rating_ver'][0])
			ver = str(apple_f1_df.loc[row, 'ver'][0])
			sup_devices = str(apple_f1_df.loc[row, 'sup_devices'][0])
			ipadSc_urls = str(apple_f1_df.loc[row, 'ipadSc_urls'][0])
			lang = str(apple_f1_df.loc[row, 'lang'][0])
			vpp_lic = str(apple_f1_df.loc[row, 'vpp_lic'][0])

			# Complex cases

			condition, app_description = get_from_another_file(apple_f2_df, 'id', app_id, 'app_desc')

			# # Removal of included entries

			apple_f2_df = apple_f2_df.drop(apple_f2_df[apple_f2_df['id'] == app_id].index)
			apple_f1_df = apple_f1_df.drop(apple_f1_df[apple_f1_df['track_name'] == track_name].index)

			if condition:

				app_description = '"app_description":' + app_description + ','

			return '', '', '"apple_apps":{' + app_description + '"version":' + ver + ',"n_of_supported_devices":' + sup_devices + ',"n_of_reviews":' + rating_count_tot + ',"n_of_ipad_urls":' + ipadSc_urls + ',"n_of_available_languages":' + lang + ',"belongs_to_volume_purchase_program":' + vpp_lic + ',"rating_curr_version":' + user_rating_ver + ',"n_of_rating_curr_version":' + rating_count_ver + ',"size":' + size_bytes + '}'

		except Exception as e:

			return '', '', ''

	if store == 1:

		global google_f1_df

		try:

			row = google_f1_df[google_f1_df['App'] == app_name].index

			# Simple cases

			app_type = str(google_f1_df.loc[row, "Type"][0])
			price = str(google_f1_df.loc[row, "Price"][0])
			curr_ver = google_f1_df.loc[row, "Current Ver"][0]
			size = google_f1_df.loc[row, "Size"][0]
			reviews = google_f1_df.loc[row, "Reviews"][0]
			android_ver = google_f1_df.loc[row, "Android Ver"][0]
			last_update = google_f1_df.loc[row, "Last Updated"][0]
			n_of_downloads = google_f1_df.loc[row, "Installs"][0]

			# Complex cases

			prices = '{"name":' + app_type + ',currencies:"[{"price":' + str(price) + '}]}'
			categories = str(category_split(google_f1_df.loc[row, "Category"][0], '_and_')) + ',' + str(category_split(google_f1_df.loc[row, "Genre"][0], '&'))

			# Removal of included entries

			google_f1_df = google_f1_df.drop(google_f1_df[google_f1_df['App'] == track_name].index)

			return categories, prices, '"google_apps":{"version":' + str(curr_ver) + ',"size":' + str(size) + ',"n_of_reviews":' + str(reviews) + ',"android_version_required":' + str(android_ver) + ',"latest_update_at_store":' + str(last_update) + ',"n_of_downloads":' + str(n_of_downloads) + '}'

		except Exception as e:

			return '', '', ''

	if store == 2:

		global shopify_f1_df
		global shopify_f2_df
		global shopify_f3_df
		global shopify_f4_df
		global shopify_f5_df
		global shopify_f6_df

		try:

			row = shopify_f1_df[shopify_f1_df['title'] == app_name].index

			# Simple cases

			app_id = shopify_f1_df.loc[row, "id"][0]
			developer = shopify_f1_df.loc[row, "developer"][0]
			developer_link = shopify_f1_df.loc[row, "developer_link"][0]
			description = shopify_f1_df.loc[row, "description"][0]
			description_raw = shopify_f1_df.loc[row, "description_raw"][0]
			url = shopify_f1_df.loc[row, "url"][0]
			tagline = shopify_f1_df.loc[row, "tagline"][0]
			icon = shopify_f1_df.loc[row, "icon"][0]
			pricing_hint = shopify_f1_df.loc[row, "pricing_hint"][0]
			reviews_count = shopify_f1_df.loc[row, "reviews_count"][0]

			# Complex cases

			condition_1, benefit_name = get_from_another_file(shopify_f4_df, 'app_id', app_id, 'title')
			condition_2, benefit_description = get_from_another_file(shopify_f4_df, 'app_id', app_id, 'description')

			categories_ids = get_vector_from_another_file(shopify_f2_df, 'app_id', app_id, 'category_id')

			categories = str(category_split(get_from_another_file(shopify_f3_df, 'id', categories_ids[0], 'title'), 'and'))

			for category_id in range(1, len(categories_ids)):
				categories = categories + str(category_split(get_from_another_file(shopify_f3_df, 'id', category_id, 'title'), 'and'))

			pricing_plan_features = get_vector_from_another_file(shopify_f5_df, 'app_id', app_id, 'feature')
			pricing_plan_ids = get_vector_from_another_file(shopify_f5_df, 'app_id', app_id, 'pricing_plan_id')

			title = str(get_from_another_file(shopify_f6_df, 'id', pricing_plan_ids[0], 'title'))
			currency_price = str(get_from_another_file(shopify_f6_df, 'id', pricing_plan_ids[0], 'price'))

			currency = ''
			price = ''

			for i in currency_price:

				if not i.isdigit() and i != '.':
					currency.append(i)

				else:
					price.append(i)

			apps_price_plans = '{"name":' + title + ',"feature":' + str(pricing_plan_features[0]) + ',"currencies": [{"currency":' + currency + ',"price":' + price + '}]}'

			for pricing_plan_id in range(1, len(pricing_plan_ids)):

				title = get_from_another_file(shopify_f6_df, 'id', pricing_plan_ids[pricing_plan_id], 'title')
				currency_price = get_from_another_file(shopify_f6_df, 'id', pricing_plan_ids[pricing_plan_id], 'price')

				for i in str(currency_price):

					if not i.isdigit() and i != '.':
						currency.append(i)

					else:
						price.append(i)

				apps_price_plans = apps_price_plans + ',{"name":' + str(title) + ',"feature":' + str(pricing_plan_features[pricing_plan_id]) + ',"currencies": [{"currency":' + str(currency) + ',"price":' + price + '}]}'

			# Removal of included entries

			shopify_f4_df = shopify_f4_df.drop(shopify_f4_df[shopify_f4_df['app_id'] == app_id].index)
			shopify_f1_df = shopify_f1_df.drop(shopify_f1_df[shopify_f1_df['title'] == track_name].index)

			if condition_1:

				benefit_name = '"benefit_name":' + benefit_name + ','

			if condition_2:

				benefit_description = '"benefit_description":' + benefit_description + ','

			return categories, apps_price_plans, '"shopify_apps":{"developer":{"name":' + str(developer) + ',"link":' + str(developer_link) + '}"app_description":' + str(description) + ',"app_raw_description":' + str(description_raw) + ',"url":' + str(url) + ',"tagline":' + str(tagline) + ',"icon":' + str(icon) + ',' + benefit_name + benefit_description + '"free_trial_days":' + str(pricing_hint) + ',"n_of_reviews":' + str(reviews_count) + '}'

		except Exception as e:

			return '', '', ''

	return '', '', ''

## END ###


### BEGIN ### Create the bulkload script file (delete the old file if it exists) and insert the main insert command

if (os.path.isfile(script_file)):
	os.remove(script_file)

script = open(script_file, "w+")

script.write('db.AppsCollection.insertMany([')

### END ###


### BEGIN ### Generate all documents for Apple apps

initial_comma = 0

for i, j in apple_f1_df.iterrows():

	# Simple cases

	app_id = str(j[0])
	track_name = str(j[1])
	currency = str(j[3])
	price = str(j[4])
	user_rating = str(j[7])
	cont_rating = str(j[10])

	# Complex cases

	categories = str(category_split(j[11], '&'))
	prices = '{"currencies:"[{"currency":' + currency + ',"price":' + price + '}]}'

	a, b, apple_data = look_app(track_name, 0) # 0 == Apple store
	goo_cat, goo_prices, google_data = look_app(track_name, 1) # 1 == Google store
	shop_cat, shop_prices, shopify_data = look_app(track_name, 2) # 2 == Shopify store

	if google_data != '':
		google_data = ',' + google_data

	if shopify_data != '':
		shopify_data = ',' + shopify_data

	if goo_cat != '':
		categories + ',' + goo_cat

	if shop_cat != '':
		categories + ',' + shop_cat

	if goo_prices != '':
		prices + ',' + goo_prices

	if shop_prices != '':
		prices + ',' + shop_prices

	document = '\n{"id":' + app_id + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"age_rating":' + cont_rating + ',"name":' + track_name + ',"rating":' + user_rating + ',' + apple_data + google_data + shopify_data + '}'

	if initial_comma == 1:
		script.write(',' + document)
	else:
		initial_comma = 1
		script.write(document)

global_id = apple_f1_df['id'].max() + 1

for i, j in google_f1_df.iterrows():

	# Simple cases

	track_name = str(j[0])
	user_rating = str(j[2])
	cont_rating = str(j[8])

	# Complex cases

	categories, prices, google_data = look_app(track_name, 1)
	shop_cat, shop_prices, shopify_data = look_app(track_name, 2)

	if shopify_data != '':
		shopify_data = ',' + shopify_data

	if shop_cat != '':
		categories + ',' + shop_cat

	if shop_prices != '':
		prices + ',' + shop_prices

	document = '\n{"id":' + str(global_id) + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"age_rating":' + cont_rating + ',"name":' + track_name + ',"rating":' + user_rating + ',' + google_data + shopify_data + '}'

	global_id = global_id + 1

	script.write(document)

for i, j in shopify_f1_df.iterrows():

	# Simple cases

	track_name = str(j[2])
	user_rating = str(j[7])

	# Complex cases

	categories, prices, shopify_data = look_app(track_name, 2)

	document = '\n{"id":' + str(global_id) + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"name":' + str(track_name) + ',"rating":' + user_rating + ',' + shopify_data + '}'

	global_id = global_id + 1

	script.write(document)

### END ###


### BEGIN ### Ends the Mongo command

script.write('])')

### END ###

'''

For each Apple app
	Populate it with the normalized data from Apple store

'''