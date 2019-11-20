#mymodule.py
################################################################################################
############ Mapping from Apple dataset to json structure ######################################
################################################################################################

'''

{
    "id" : <id>,
    "categories" : ["<prime_genre>", ...], (Remember to break the composed genres)
    "apps_price_plans" : [{"currencies: " [{"currency" : "<currency>", "price" : <price>}]}],
    "age_rating" : <cont_rating>,
    "name" : <track_name>, (Verify if this name already exists in Google or Shopify stores)
    "rating" : <user_rating>,
    "apple_apps" :
    {
        "app_description" : <app_description>, (Get from appleStore_description.csv by app id)
        "version" : <ver>,
        "n_of_supported_devices" :<sup_devices>,
        "n_of_reviews" : <rating_count_tot>,
        "n_of_ipad_urls" : <ipadSc_urls>,
        "n_of_available_languages" : <lang>,
        "belongs_to_volume_purchase_program" : <vpp_lic>,
        "rating_curr_version" : <user_rating_ver>,
        "n_of_rating_curr_version" : <rating_count_ver>,
        "size" : <size_bytes>
    }
}


'''


################################################################################################
############ Mapping from Google dataset to json structure #####################################
################################################################################################

'''

{
	"id" : <id>, (Generate the Google app ids with the Joao formule)
	"categories" : [{"name" : <Category>},{"name" : <Genres>}], (Remember to break the composed genres and categories)
	"apps_price_plans" : [{"name" : <Type>, "currencies" : [{"price" : <Price>}]}],
	"age_rating" : <Content Rating>, (Remember to create a value accordingly to age rating category)
	"name" : <App>, (Verify if this name already exists in Shopify store)
	"rating" : <Rating>,
	"google_apps" :
	{
		"version" : <Current Ver>,
		"size" : <Size>, (Convert from Megabytes to bytes)
		"n_of_reviews" : <Reviews>,
		"android_version_required" : <Android Ver>,
		"latest_update_at_store" : <Last Updated>,
		"n_of_downloads" : <Installs>
	}
}

'''


################################################################################################
############ Mapping from Shopify dataset to json structure ####################################
################################################################################################

'''

{
	"id" : <id>, (Verify if this id already exists and get the greatest id in the dataset plus one)
	"categories" : [{"name" : <title>}], (Get the id attribute from apps file; get all category_id on apps_categories that is attached to app id; get the corresponding category name for the obtained category ids on categories file)
	"apps_price_plans" : [{"name" : <title>, (Get the id attribute from apps file; get the corresponding plan name from pricing_plans file)
						  "feature" : <feature>, (Get the id attribute from apps file; get the corresponding plan feature from pricing_plan_feature file)
						  "currencies" : [{"currency" : <price>, (Get the id attribute from apps file; get the corresponding currency from pricing_plans file. Ignore the price)
						  				  "price" : <price>}]}] (Get the id attribute from apps file; get the corresponding price from pricing_plans file. Ignore the price currency and period; convert strings to values)
	"name" : <title>,
	"rating" : <rating>,
	"shopify_apps" :
	{
			"developer" : {"name" : <developer>, "link" : <developer_link>}
            "app_description" : <description>,
            "app_raw_description" : <description_raw>,
            "url" : <url>,
            "tagline" : <tagline>,
            "icon" : <icon>,
            "benefit_name" : <title>, (Get the id attribute from apps file; get the corresponding benefit name from key_benefits file)
            "benefit_description" : <description>, (Get the id attribute from apps file; get the corresponding benefit description from key_benefits file)
            "free_trial_days" : <pricing_hint>,
            "n_of_reviews" : <reviews_count>
	}
}

'''


################################################################################################
############ Import libraries to manipulate the csv files ######################################
################################################################################################

import pandas as pd
import os
import re


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

def str_convert(s):
	return re.sub('[^A-Za-z0-9 ]+', '', str(s))

def category_splitter(content, splitter):

	content_vector = content.split(splitter)

	categories = '"' + str_convert(content_vector[0]) + '"'

	for i in range(1, len(content_vector)):
		categories = categories + ', "' + str_convert(content_vector[i]) + '"'

	return categories

def look_apple_app(app_name):

	global apple_f1_df
	global apple_f2_df

	############ Simple cases for File 1 ############

	row = (apple_f1_df[apple_f1_df['track_name'] == app_name].index)[0]

	size_bytes = str_convert(apple_f1_df.at[row, 'size_bytes'])
	rating_count_tot = str_convert(apple_f1_df.at[row, 'rating_count_tot'])
	rating_count_ver = str_convert(apple_f1_df.at[row, 'rating_count_ver'])
	user_rating_ver = str_convert(apple_f1_df.at[row, 'user_rating_ver'])
	ver = str_convert(apple_f1_df.at[row, 'ver'])
	sup_devices = str_convert(apple_f1_df.at[row, 'sup_devices.num'])
	ipadSc_urls = str_convert(apple_f1_df.at[row, 'ipadSc_urls.num'])
	lang = str_convert(apple_f1_df.at[row, 'lang.num'])
	vpp_lic = str_convert(apple_f1_df.at[row, 'vpp_lic'])
	currency = str_convert(apple_f1_df.at[row, 'currency'])
	price = str_convert(apple_f1_df.at[row, 'price'])

	############ Complex cases for File 1 ############

	categories = category_splitter(apple_f1_df.at[row, 'prime_genre'], '&')

	apple_f1_df = apple_f1_df.drop(row)

	############ Simple cases for File 2 ############

	row = (apple_f2_df[apple_f2_df['track_name'] == app_name].index)[0]

	app_description = str_convert(apple_f2_df.at[row, 'app_desc'])

	prices = '{\n"currencies" : [\n{\n"currency" : "' + currency + '",\n"price" : ' + price + '\n}\n]\n}'

	apple_f2_df = apple_f2_df.drop(row)

	############ Final document ############

	return categories, prices, '"apple_apps" : {\n"app_description" : "' + app_description + '",\n"version" : "' + ver + '",\n"n_of_supported_devices" : ' + sup_devices + ',\n"n_of_reviews" : ' + rating_count_tot + ',\n"n_of_ipad_urls" : ' + ipadSc_urls + ',\n"n_of_available_languages" : ' + lang + ',\n"belongs_to_volume_purchase_program" : ' + vpp_lic + ',\n"rating_curr_version" : ' + user_rating_ver + ',\n"n_of_rating_curr_version" : ' + rating_count_ver + ',\n"size" : ' + size_bytes + '\n}'

def look_google_app(app_name):

	global google_f1_df

	############ Simple cases for File 1 ############

	row = google_f1_df[google_f1_df['App'] == app_name].index

	if not len(row):
		return '', '', ''

	row = row[0]

	app_type = str_convert(google_f1_df.at[row, "Type"])
	price = str_convert(google_f1_df.at[row, "Price"])
	curr_ver = str_convert(google_f1_df.at[row, "Current Ver"])
	size = str_convert(google_f1_df.at[row, "Size"])
	reviews = str_convert(google_f1_df.at[row, "Reviews"])
	android_ver = str_convert(google_f1_df.at[row, "Android Ver"])
	last_update = str_convert(google_f1_df.at[row, "Last Updated"])
	n_of_downloads = str_convert(google_f1_df.at[row, "Installs"])

	############ Complex cases for File 1 ############

	# prices = '{"name" : "' + app_type + '", "currencies" : "[{"price" : ' + price + '}]}'
	prices = '{\n"name" : "' + app_type + '", "currencies" : [\n{\n"price" : ' + price + '\n}\n]\n}'

	categories = category_splitter(google_f1_df.at[row, "Category"], '_and_')
	categories = categories + ',' + category_splitter(google_f1_df.at[row, "Genres"], '&')

	google_f1_df = google_f1_df.drop(row)

	############ Final document ############

	return categories, prices, '\n"google_apps" : {\n"version" : "' + curr_ver + '",\n"size" : "' + size + '",\n"n_of_reviews" : ' + reviews + ',\n"android_version_required" : "' + android_ver + '",\n"latest_update_at_store" : "' + last_update + '",\n"n_of_downloads" : ' + n_of_downloads + '\n}'

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
	name = str_convert(shopify_f1_df.at[row, "title"])
	developer = str_convert(shopify_f1_df.at[row, "developer"])
	developer_link = str_convert(shopify_f1_df.at[row, "developer_link"])
	description = str_convert(shopify_f1_df.at[row, "description"])
	description_raw = str_convert(shopify_f1_df.at[row, "description_raw"])
	url = str_convert(shopify_f1_df.at[row, "url"])
	tagline = str_convert(shopify_f1_df.at[row, "tagline"])
	icon = str_convert(shopify_f1_df.at[row, "icon"])
	pricing_hint = str_convert(shopify_f1_df.at[row, "pricing_hint"])
	reviews_count = str_convert(shopify_f1_df.at[row, "reviews_count"])

	shopify_f1_df = shopify_f1_df.drop(row)

	############ Complex cases for Files 2 and 3 ############

	rows = shopify_f2_df.loc[shopify_f2_df['app_id'] == app_id, ['category_id']].index

	categories = ''
	comma = ''

	if len(rows):
		for cat_id_row in range(len(rows)):
			category_id = shopify_f2_df.at[cat_id_row, "category_id"]
			cat_title_row = (shopify_f3_df[shopify_f3_df['id'] == category_id].index)[0]
			categories = categories + comma + category_splitter(shopify_f3_df.at[cat_title_row, "title"], ' and ')
			comma = ', '
		print(categories)

	############ Complex cases for File 4 ############

	row = shopify_f4_df[shopify_f4_df['app_id'] == app_id].index

	if len(row):
		benefit_name = '",\n"benefit_name" : "' + str_convert(shopify_f4_df.at[row[0], 'title'])
		benefit_description = '",\n"benefit_description" : "' + (str_convert(shopify_f4_df.at[row[0], 'description']))
	else:
		benefit_name = ''
		benefit_description = ''

	############ Complex cases for Files 5 and 6 ############

	rows = shopify_f5_df.loc[shopify_f5_df['app_id'] == app_id, ['pricing_plan_id']].index

	prices = ''
	comma = ''

	if len(rows):
		for plans_id_row in range(len(rows)):
			plan_feature = str_convert(shopify_f5_df.at[plans_id_row, "feature"])

			plan_id = shopify_f5_df.at[plans_id_row, "pricing_plan_id"]
			plan_row = (shopify_f6_df[shopify_f6_df['id'] == plan_id].index)[0]
			plan_title = str_convert(shopify_f6_df.at[plan_row, "title"])
			plan_currency_price = str_convert(shopify_f6_df.at[plan_row, "title"])

			plan_currency = ''
			plan_price = ''

			for i in plan_currency_price:

				if not i.isdigit() and i != '.':
					plan_currency = plan_currency + i
				else:
					plan_price = plan_price + i

			prices = prices + comma + '{\n"name" : "' + plan_title + '"\n"feature" : "' + plan_feature + '"\n"currencies" : [\n{\n"currency" : "' + plan_currency + '",\n"price" : ' + plan_price + '\n}\n]\n}'
			comma = ','

	############ Final document ############

	return categories, prices, '\n"shopify_apps" : {\n"developer" : {\n"name" : "' + developer + '",\n"link" : "' + developer_link + '"},\n"app_description" : "' + description + '",\n"app_raw_description" : "' + description_raw + '",\n"url" : "' + url + '",\n"tagline" : "' + tagline + '",\n"icon" : "' + icon + benefit_name + benefit_description + '",\n"free_trial_days" : "' + pricing_hint + '",\n"n_of_reviews" : ' + reviews_count + '\n}'


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

comma = ''

for i, j in apple_f1_df.iterrows():

	############ Simple cases ############

	app_id = str_convert(j[0])
	track_name = str(j[1])
	user_rating = str_convert(j[7])
	cont_rating = str_convert(j[10])

	############ Complex cases ############

	categories, prices, apple_data = look_apple_app(track_name)
	g_categories, g_prices, g_data = look_google_app(track_name)
	s_categories, s_prices, s_data = look_shopify_app(track_name)

	if g_categories != '':
		categories + ',' + g_categories

	if g_prices != '':
		prices + ',' + g_prices

	if g_data != '':
		g_data = ',' + g_data

	if s_categories != '':
		categories + ',' + s_categories

	if s_prices != '':
		prices + ',' + s_prices

	if s_data != '':
		s_data = ',' + s_data

	document = comma + '{\n"id" : ' + app_id + ',\n"categories" : [' + categories + '],\n"apps_price_plans" : [' + prices + '],\n"age_rating" : "' + cont_rating + '",\n"name" : "' + str_convert(track_name) + '",\n"rating" : ' + user_rating + ',\n' + apple_data + g_data + s_data + '\n}'

	script.write(document)

	comma = ',\n'

global_id = apple_f1_df['id'].max() + 1

for i, j in google_f1_df.iterrows():

	############ Simple cases ############

	app = str(j[0])
	rating = str_convert(j[2])
	content_rating = str_convert(j[8])

	############ Complex cases ############

	categories, prices, google_data = look_google_app(app)
	s_categories, s_prices, s_data = look_shopify_app(app)

	if s_categories != '':
		categories + ',' + s_categories

	if s_prices != '':
		prices + ',' + s_prices

	if s_data != '':
		s_data = ',' + s_data

	document = ',\n{\n"id" : ' + str_convert(global_id) + ', "categories" : [' + categories + '], "apps_price_plans" : [' + prices + '], "age_rating" : "' + content_rating + '", "name" : "' + str_convert(app) + '", "rating" : ' + rating + ',' + google_data + s_data + '}'

	global_id = global_id + 1

	script.write(document)

for i, j in shopify_f1_df.iterrows():

	############ Simple cases ############

	title = str(j[2])
	user_rating = str_convert(j[7])

	############ Complex cases ############

	categories, prices, shopify_data = look_shopify_app(title)

	document = ',\n{\n"id" : ' + str_convert(global_id) + ', "categories" : [' + categories + '], "apps_price_plans" : [' + prices + '], "name" : "' + str_convert(title) + '", "rating" : ' + str(int(user_rating)/10) + ', ' + shopify_data + '}'

	global_id = global_id + 1

	script.write(document)


################################################################################################
############ Ends the Mongo command
################################################################################################

script.write('])')