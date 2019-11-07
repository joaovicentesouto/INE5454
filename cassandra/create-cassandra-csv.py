import pandas as pd
import numpy as np
import uuid

###################################################################################
# Load Files and Change column names
###################################################################################

print("Loading bulk load")

# Bulk load
bulk_load = pd.read_csv("csvs/bulk_load.csv", sep=';')

print("Loading Apple")

# APPLE
apple_apps = pd.read_csv("../datasets/apple/apps.csv")

columns = [
	'size_bytes',
	'currency',
	'price',
	'rating_count_tot',
	'rating_count_ver',
	'user_rating',
	'user_rating_ver',
	'ver',
	'cont_rating',
	'prime_genre',
	'sup_devices.num',
	'ipadSc_urls.num',
	'lang.num',
	'vpp_lic'
]
apple_apps.drop(columns, inplace=True, axis=1)

apple_apps.rename(
	columns = {'id':'app_id', 'track_name':'app_name'},
	inplace = True
)

apple_reviews = pd.read_csv("../datasets/apple/reviews.csv")
apple_reviews.rename(
	columns = {'id':'app_id', 'review':'content'},
	inplace = True
)

print("Loading Google")

# GOOGLE
google_reviews = pd.read_csv("../datasets/google/reviews.csv")
google_reviews.rename(
	columns = {
		'App':'app_name',
		'Translated_Review':'content',
		'Sentiment':'sentiment_type',
		'Sentiment_Polarity':'sentiment_polarity',
		'Sentiment_Subjectivity':'sentiment_subjectivity'
	},
	inplace = True
)
google_reviews['app_id'] = int(0)

print("Loading Shopify")

# SHOPIFY
shopify_apps = pd.read_csv("../datasets/shopify/apps.csv")

columns = [
	'url',
	'tagline',
	'developer',
	'developer_link',
	'icon',
	'rating',
	'reviews_count',
	'description',
	'description_raw',
	'pricing_hint'
]
shopify_apps.drop(columns, inplace=True, axis=1)

shopify_apps.rename(
	columns = {'id':'app_id', 'title':'app_name'},
	inplace = True
)

shopify_reviews = pd.read_csv("../datasets/shopify/reviews.csv")
shopify_reviews.rename(
	columns = {
		'id':'app_id',
		'body':'content',
		'posted_at':'post_date',
		'developer_reply_posted_at':'developer_reply_post_date'
	},
	inplace = True
)

###################################################################################
# Transform app name to lowercase
###################################################################################

print("Preprocessing")

# Preprocess
apple_apps['app_name']     = apple_apps['app_name'].map(lambda x : x.lower())
google_reviews['app_name'] = google_reviews['app_name'].map(lambda x : x.lower())
shopify_apps['app_name']   = shopify_apps['app_name'].map(lambda x : x.lower())

###################################################################################
# Build default date type
###################################################################################

def build_date(date):
	if not isinstance(date, str):
		return np.nan

	date = date.replace(",", "").split(" ")

	new_date = date[2] + "-"

	if date[0] == 'January':
		new_date = new_date + '01'
	elif date[0] == 'February':
		new_date = new_date + '02'
	elif date[0] == 'March':
		new_date = new_date + '03'
	elif date[0] == 'April':
		new_date = new_date + '04'
	elif date[0] == 'May':
		new_date = new_date + '05'
	elif date[0] == 'June':
		new_date = new_date + '06'
	elif date[0] == 'July':
		new_date = new_date + '07'
	elif date[0] == 'August':
		new_date = new_date + '08'
	elif date[0] == 'September':
		new_date = new_date + '09'
	elif date[0] == 'October':
		new_date = new_date + '20'
	elif date[0] == 'November':
		new_date = new_date + '11'
	elif date[0] == 'December':
		new_date = new_date + '12'
	else:
		new_date = new_date + '00'

	if int(date[1]) < 10:
		return new_date + "-0" + date[1]
		
	return new_date + "-" + date[1]

for index, row in shopify_reviews.iterrows():
	print("Shopify Preprocess:", index)

	shopify_reviews.loc[index, 'post_date'] = build_date(row['post_date'])
	shopify_reviews.loc[index, 'developer_reply_post_date'] = build_date(row['developer_reply_post_date'])

###################################################################################
# Updates app IDs
###################################################################################

# Updates App IDs
initial_max = apple_apps['app_id'].max()
max_id = initial_max

print("Max INDEX:", max_id)

for index, row in google_reviews.iterrows():
	print("Update Google:", index)

	if row['app_name'] in apple_apps['app_name'].values:
		if  row['app_id'] == 0:
			google_reviews.loc[google_reviews['app_id'] == row['app_id'], 'app_id'] = apple_apps[apple_apps['app_name'] == row['app_name']]['app_id'].values[0]
	else:
		max_id += 1
		google_reviews.loc[google_reviews['app_name'] == row['app_name'], 'app_id'] = int(max_id)

# google_reviews['app_id'] = google_reviews['app_id'].astype(int)

print("Update shopify id")

for index, row in shopify_apps.iterrows():
	print("Update Shopify:", index)

	if row['app_name'] in apple_apps['app_name'].values:
		new_id = apple_apps[apple_apps['app_name'] == row['app_name']]['app_id'].values[0]

		shopify_reviews.loc[shopify_reviews['app_id'] == row['app_id'], 'app_id'] = new_id

		shopify_apps.loc[index, 'app_ip'] = new_id
	else:
		if row['app_name'] in google_reviews['app_name'].values:
			new_id = google_reviews[google_reviews['app_name'] == row['app_name']]['app_id'].values[0]

			shopify_reviews.loc[shopify_reviews['app_id'] == row['app_id'], 'app_id'] = new_id

			shopify_apps.loc[index, 'app_ip'] = new_id
		else:
			max_id += 1

			shopify_reviews.loc[shopify_reviews['app_id'] == row['app_id'], 'app_id'] = max_id

			shopify_apps.loc[index, 'app_ip'] = max_id

###################################################################################
# Create the csv to bulk load
###################################################################################

# Buld bulk load

for index, row in apple_reviews.iterrows():
	print("Adds apple reviews:", index)

	if apple_reviews.loc[index, 'content'] == np.nan:
		continue

	content = str(apple_reviews.loc[index, 'content']).replace("\n", " ").replace(";", ":")

	if content == 'nan':
		continue

	new_row = [
		uuid.uuid4(),
		apple_reviews.loc[index, 'app_id'],
		np.nan,
		np.nan,
		np.nan,
		np.nan,
		content,
		np.nan,
		np.nan,
		np.nan,
		np.nan,
		np.nan
	]

	bulk_load.loc[bulk_load.index.max()+1] = new_row

for index, row in google_reviews.iterrows():
	print("Adds google reviews:", index)

	if google_reviews.loc[index, 'content'] == np.nan:
		continue

	content = str(google_reviews.loc[index, 'content']).replace("\n", " ").replace(";", ":")

	if content == 'nan':
		continue

	new_row = [
		uuid.uuid4(),
		google_reviews.loc[index, 'app_id'],
		google_reviews.loc[index, 'sentiment_type'],
		google_reviews.loc[index, 'sentiment_polarity'],
		google_reviews.loc[index, 'sentiment_subjectivity'],
		np.nan,
		content,
		np.nan,
		np.nan,
		np.nan,
		np.nan,
		np.nan
	]

	bulk_load.loc[bulk_load.index.max()+1] = new_row

for index, row in shopify_reviews.iterrows():
	print("Adds shopify reviews:", index)

	if shopify_reviews.loc[index, 'content'] != np.nan and str(shopify_reviews.loc[index, 'content']) == 'nan':
		continue

	content = str(shopify_reviews.loc[index, 'content']).replace("\n", " ").replace(";", ":")

	if content == 'nan':
		continue

	new_row = [
		uuid.uuid4(),
		shopify_reviews.loc[index, 'app_id'],
		np.nan,
		np.nan,
		np.nan,
		shopify_reviews.loc[index, 'author'],
		content,
		shopify_reviews.loc[index, 'rating'],
		shopify_reviews.loc[index, 'helpful_count'],
		shopify_reviews.loc[index, 'post_date'],
		shopify_reviews.loc[index, 'developer_reply'],
		shopify_reviews.loc[index, 'developer_reply_post_date']
	]

	bulk_load.loc[bulk_load.index.max()+1] = new_row

print("Saving CSV")

bulk_load.to_csv('csvs/cassandra_bulk_load.csv', sep=';', encoding='utf-8', index=False)