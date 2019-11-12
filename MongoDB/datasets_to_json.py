#mymodule.py

################################################################################################
############ Mapping from Apple dataset to json structure ######################################
################################################################################################

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


################################################################################################
############ Mapping from Google dataset to json structure #####################################
################################################################################################

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


################################################################################################
############ Mapping from Shopify dataset to json structure ####################################
################################################################################################

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


################################################################################################
############ Import libraries to manipulate the csv files ######################################
################################################################################################

import pandas as pd
import os


################################################################################################
############ Definition of all files used in this script #######################################
################################################################################################

apple_file1 = '../datasets/Apple/AppleStore.csv'
apple_file2 = '../datasets/Apple/appleStore_description.csv'

google_file1 = '../datasets/Google/googleplaystore.csv'

shopify_file1 = '../datasets/Shopify/apps.csv'
shopify_file2 = '../datasets/Shopify/apps_categories.csv'
shopify_file3 = '../datasets/Shopify/categories.csv'
shopify_file4 = '../datasets/Shopify/key_benefits.csv'
shopify_file5 = '../datasets/Shopify/pricing_plan_features.csv'
shopify_file6 = '../datasets/Shopify/pricing_plans.csv'

script_file = './MongoDB_bulkLoad.js'


################################################################################################
############ Tries to open all necessary datasets ##############################################
################################################################################################

try:

	apple_f1_df = pd.read_csv(apple_file1, sep=',', quotechar='"', encoding='utf8')
	apple_f2_df = pd.read_csv(apple_file2, sep=',', quotechar='"', encoding='utf8')
	google_f1_df = pd.read_csv(google_file1, sep=',', quotechar='"', encoding='utf8')
	shopify_f1_df = pd.read_csv(shopify_file1, sep=',', quotechar='"', encoding='utf8')
	shopify_f2_df = pd.read_csv(shopify_file2, sep=',', quotechar='"', encoding='utf8')
	shopify_f3_df = pd.read_csv(shopify_file3, sep=',', quotechar='"', encoding='utf8')
	shopify_f4_df = pd.read_csv(shopify_file4, sep=',', quotechar='"', encoding='utf8')
	shopify_f5_df = pd.read_csv(shopify_file5, sep=',', quotechar='"', encoding='utf8')
	shopify_f6_df = pd.read_csv(shopify_file6, sep=',', quotechar='"', encoding='utf8')
	
except IOError:

	print('Was not able to open some dataset. Please check!')
	exit(1)


################################################################################################
############ Normalizes the datasets ###########################################################
################################################################################################

apple_f1_df['track_name'] 		= apple_f1_df['track_name'].map(lambda x : x.lower())
apple_f1_df['prime_genre']   	= apple_f1_df['prime_genre'].map(lambda x : x.lower())

apple_f2_df['track_name']   = apple_f2_df['track_name'].map(lambda x : x.lower())
apple_f2_df['app_desc']   	= apple_f2_df['app_desc'].map(lambda x : x.lower())

google_f1_df['App']   			= google_f1_df['App'].map(lambda x : x.lower())
google_f1_df['Category']   		= google_f1_df['Category'].map(lambda x : x.lower())
google_f1_df['Reviews']   		= google_f1_df['Reviews'].map(lambda x : x.lower())
google_f1_df['Size']   			= google_f1_df['Size'].map(lambda x : x.lower())
google_f1_df['Installs']   		= google_f1_df['Installs'].map(lambda x : x.lower())
google_f1_df['Genres']   		= google_f1_df['Genres'].map(lambda x : x.lower())
google_f1_df['Last Updated']   	= google_f1_df['Last Updated'].map(lambda x : x.lower())

shopify_f1_df['url']   				= shopify_f1_df['url'].map(lambda x : x.lower())
shopify_f1_df['title']   			= shopify_f1_df['title'].map(lambda x : x.lower())
shopify_f1_df['tagline']   			= shopify_f1_df['tagline'].map(lambda x : x.lower())
shopify_f1_df['developer']   		= shopify_f1_df['developer'].map(lambda x : x.lower())
shopify_f1_df['developer_link'] 	= shopify_f1_df['developer_link'].map(lambda x : x.lower())
shopify_f1_df['icon']   			= shopify_f1_df['icon'].map(lambda x : x.lower())
shopify_f1_df['description']   		= shopify_f1_df['description'].map(lambda x : x.lower())
shopify_f1_df['description_raw']	= shopify_f1_df['description_raw'].map(lambda x : x.lower())

shopify_f3_df['title']	= shopify_f3_df['title'].map(lambda x : x.lower())

shopify_f4_df['title']   		= shopify_f4_df['title'].map(lambda x : x.lower())
shopify_f4_df['description']	= shopify_f4_df['description'].map(lambda x : x.lower())

shopify_f5_df['feature']   			= shopify_f5_df['feature'].map(lambda x : x.lower())


################################################################################################
############ Auxiliar methods ##################################################################
################################################################################################

def category_splitter(content, splitter):

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

def look_apple_app(app_name):

	global apple_f1_df
	global apple_f2_df

	############ Simple cases for File 1 ############

	row = (apple_f1_df[apple_f1_df['track_name'] == app_name].index)[0]

	size_bytes = str(apple_f1_df.at[row, 'size_bytes'])
	rating_count_tot = str(apple_f1_df.at[row, 'rating_count_tot'])
	rating_count_ver = str(apple_f1_df.at[row, 'rating_count_ver'])
	user_rating_ver = str(apple_f1_df.at[row, 'user_rating_ver'])
	ver = str(apple_f1_df.at[row, 'ver'])
	sup_devices = str(apple_f1_df.at[row, 'sup_devices.num'])
	ipadSc_urls = str(apple_f1_df.at[row, 'ipadSc_urls.num'])
	lang = str(apple_f1_df.at[row, 'lang.num'])
	vpp_lic = str(apple_f1_df.at[row, 'vpp_lic'])
	currency = str(apple_f1_df.at[row, 'currency'])
	price = str(apple_f1_df.at[row, 'price'])

	############ Complex cases for File 1 ############

	categories = category_splitter(str(apple_f1_df.at[row, 'prime_genre']), '&')

	apple_f1_df = apple_f1_df.drop(row)

	############ Simple cases for File 2 ############

	row = (apple_f2_df[apple_f2_df['track_name'] == app_name].index)[0]

	app_description = apple_f2_df.at[row, 'app_desc']

	prices = '{"currencies:"[{"currency":' + currency + ',"price":' + price + '}]}'

	apple_f2_df = apple_f2_df.drop(row)

	############ Final document ############

	return categories, prices, '"apple_apps":{"app_description":' + app_description + ',"version":' + ver + ',"n_of_supported_devices":' + sup_devices + ',"n_of_reviews":' + rating_count_tot + ',"n_of_ipad_urls":' + ipadSc_urls + ',"n_of_available_languages":' + lang + ',"belongs_to_volume_purchase_program":' + vpp_lic + ',"rating_curr_version":' + user_rating_ver + ',"n_of_rating_curr_version":' + rating_count_ver + ',"size":' + size_bytes + '}'

def look_google_app(app_name):

	global google_f1_df

	############ Simple cases for File 1 ############

	row = google_f1_df[google_f1_df['App'] == app_name].index

	if not len(row):
		return '', '', ''

	row = row[0]

	app_type = str(google_f1_df.at[row, "Type"])
	price = str(google_f1_df.at[row, "Price"])
	curr_ver = str(google_f1_df.at[row, "Current Ver"])
	size = str(google_f1_df.at[row, "Size"])
	reviews = str(google_f1_df.at[row, "Reviews"])
	android_ver = str(google_f1_df.at[row, "Android Ver"])
	last_update = str(google_f1_df.at[row, "Last Updated"])
	n_of_downloads = str(google_f1_df.at[row, "Installs"])

	############ Complex cases for File 1 ############

	prices = '{"name":' + app_type + ',currencies:"[{"price":' + price + '}]}'

	categories = category_splitter(str(google_f1_df.at[row, "Category"]), '_and_')
	categories = categories + ',' + category_splitter(str(google_f1_df.at[row, "Genres"]), '&')

	google_f1_df = google_f1_df.drop(row)

	############ Final document ############

	return categories, prices, '"google_apps":{"version":' + curr_ver + ',"size":' + size + ',"n_of_reviews":' + reviews + ',"android_version_required":' + android_ver + ',"latest_update_at_store":' + last_update + ',"n_of_downloads":' + n_of_downloads + '}'

def look_shopify_app(app_name):

	global shopify_f1_df
	global shopify_f2_df
	global shopify_f3_df
	global shopify_f4_df
	global shopify_f5_df
	global shopify_f6_df

	############ Simple cases for File 1 ############

	row = shopify_f1_df[shopify_f1_df['title'] == app_name].index

	if not len(row):
		return '', '', ''

	row = row[0]

	app_id = shopify_f1_df.at[row, "id"]
	name = str(shopify_f1_df.at[row, "title"])
	developer = str(shopify_f1_df.at[row, "developer"])
	developer_link = str(shopify_f1_df.at[row, "developer_link"])
	description = str(shopify_f1_df.at[row, "description"])
	description_raw = str(shopify_f1_df.at[row, "description_raw"])
	url = str(shopify_f1_df.at[row, "url"])
	tagline = str(shopify_f1_df.at[row, "tagline"])
	icon = str(shopify_f1_df.at[row, "icon"])
	pricing_hint = str(shopify_f1_df.at[row, "pricing_hint"])
	reviews_count = str(shopify_f1_df.at[row, "reviews_count"])

	shopify_f1_df = shopify_f1_df.drop(row)

	############ Complex cases for Files 2 and 3 ############

	rows = shopify_f2_df.loc[shopify_f2_df['app_id'] == app_id, ['category_id']].index

	categories = ''

	if len(rows):
		for cat_id_row in range(len(rows)):
			category_id = shopify_f2_df.at[cat_id_row, "category_id"]
			cat_title_row = (shopify_f3_df[shopify_f3_df['id'] == category_id].index)[0]
			categories = categories + category_splitter(str(shopify_f3_df.at[cat_title_row, "title"]), 'and')

	############ Complex cases for File 4 ############

	row = shopify_f4_df[shopify_f4_df['app_id'] == app_id].index

	if len(row):
		benefit_name = ',"benefit_name":' + str(shopify_f4_df.at[row[0], 'title'])
		benefit_description = ',"benefit_description":' + str(shopify_f4_df.at[row[0], 'description'])
	else:
		benefit_name = ''
		benefit_description = ''

	############ Complex cases for Files 5 and 6 ############

	rows = shopify_f5_df.loc[shopify_f5_df['app_id'] == app_id, ['pricing_plan_id']].index

	prices = ''

	if len(rows):
		for plans_id_row in range(len(rows)):
			plan_feature = shopify_f5_df.at[plans_id_row, "feature"]

			plan_id = shopify_f5_df.at[plans_id_row, "pricing_plan_id"]
			plan_row = (shopify_f6_df[shopify_f6_df['id'] == plan_id].index)[0]
			plan_title = str(shopify_f6_df.at[plan_row, "title"])
			plan_currency_price = str(shopify_f6_df.at[plan_row, "title"])

			plan_currency = ''
			plan_price = ''

			for i in plan_currency_price:

				if not i.isdigit() and i != '.':
					plan_currency = plan_currency + i
				else:
					plan_price = plan_price + i

			prices = prices + '{"name":' + plan_title + ',"feature":' + plan_feature + ',"currencies:[{"currency:"' + plan_currency + ',"price":' + plan_price + '}]}'

	############ Final document ############

	return categories, prices, '"shopify_apps":{"developer":{"name":' + developer + ',"link":' + developer_link + '}"app_description":' + description + ',"app_raw_description":' + description_raw + ',"url":' + url + ',"tagline":' + tagline + ',"icon":' + icon + benefit_name + benefit_description + ',"free_trial_days":' + pricing_hint + ',"n_of_reviews":' + reviews_count + '}'


################################################################################################
############ Create the bulkload script file (delete the old file if it exists) and insert the main insert command
################################################################################################

if (os.path.isfile(script_file)):
	os.remove(script_file)

script = open(script_file, "w+")

script.write('db.AppsCollection.insertMany([')


################################################################################################
############ Generate all documents for Apple apps
################################################################################################

first_comma = 0

# for i, j in apple_f1_df.iterrows():

# 	############ Simple cases ############

# 	app_id = str(j[0])
# 	track_name = str(j[1])
# 	user_rating = str(j[7])
# 	cont_rating = str(j[10])

# 	############ Complex cases ############

# 	categories, prices, apple_data = look_apple_app(track_name)
# 	g_categories, g_prices, g_data = look_google_app(track_name)
# 	s_categories, s_prices, s_data = look_shopify_app(track_name)

# 	if g_categories != '':
# 		categories + ',' + g_categories

# 	if g_prices != '':
# 		prices + ',' + g_prices

# 	if g_data != '':
# 		g_data = ',' + g_data

# 	if s_categories != '':
# 		categories + ',' + s_categories

# 	if s_prices != '':
# 		prices + ',' + s_prices

# 	if s_data != '':
# 		s_data = ',' + s_data

# 	document = '\n{"id":' + app_id + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"age_rating":' + cont_rating + ',"name":' + track_name + ',"rating":' + user_rating + ',' + apple_data + '}' + g_data + s_data + '}'

# 	if first_comma == 1:
# 		script.write(',' + document)
# 	else:
# 		first_comma = 1
# 		script.write(document)

global_id = apple_f1_df['id'].max() + 1

for i, j in google_f1_df.iterrows():

	############ Simple cases ############

	app = str(j[0])
	rating = str(j[2])
	content_rating = str(j[8])

	############ Complex cases ############

	categories, prices, google_data = look_google_app(app)
	s_categories, s_prices, s_data = look_shopify_app(app)

	if s_categories != '':
		categories + ',' + s_categories

	if s_prices != '':
		prices + ',' + s_prices

	if s_data != '':
		s_data = ',' + s_data

	document = '\n{"id":' + str(global_id) + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"age_rating":' + content_rating + ',"name":' + app + ',"rating":' + rating + ',' + google_data + s_data + '}'

	global_id = global_id + 1

	script.write(',' + document)

exit(0)

for i, j in shopify_f1_df.iterrows():

	############ Simple cases ############

	title = str(j[2])
	user_rating = str(j[7])

	############ Complex cases ############

	categories, prices, shopify_data = look_shopify_app(title)

	document = '\n{"id":' + str(global_id) + ',"categories":[' + categories + '],"apps_price_plans":[' + prices + '],"name":' + title + ',"rating":' + user_rating + ',' + shopify_data + '}'

	global_id = global_id + 1

	script.write(',' + document)


################################################################################################
############ Ends the Mongo command
################################################################################################

script.write('])')