
### BEGIN ### Import libraries to manipulate the csv files

import pandas as pd

### END ###

### BEGIN ### Mapping from Apple dataset to json structure
'''

{
    "id": <id>,
    "categories": [{"name": <prime_genre>}], (Remember to break the composed genres)
    "apps_price_plans": [[{"currency": <currency>,"price": <price>}]],
    "age_rating": <cont_rating>,
    "name": <track_name>,
    "rating": <user_rating>,
    "apple_apps":
    {
        "app_description": <app_description>, (Get from appleStore_description.csv by app id)
        "version": <ver>,
        "n_of_supported_devices":<sup_devices.num>,
        "n_of_reviews": <rating_count_tot>,
        "n_of_ipad_urls": <ipadSc_urls.num>,
        "n_of_available_languages": <lang.num>,
        "belongs_to_volume_purchase_program": <vpp_lic>,
        "rating_curr_version": <user_rating_ver>,
        "n_of_rating_curr_version": <rating_count_ver>,
        "size": <size_bytes>
    }
}

 .
 .
 .

Complete with mapping of Google and Shopify structures

'''
### END ###

'''

Open all datasets

create a JavaScript file with mongoDB command to insert all the documents

For each Apple app
	create a Json structure
	Populate it with the normalized data from Apple store
	Look at Shopify and Google store by Apple app name
	If this app exist in another stores
		Create another store on Json
		Populate it with the normalized data from another stores
		Delete this app from another stores
	Append the generated document at JavaScript file

For each Google app
	create a Json structure
	Populate it with the normalized data from Google store
	Look at Shopify store by Google app name
	If this app exist in Shopify store
		Create a Shopify store on Json
		Populate it with the normalized data from Shopify store
		Delete this app from Shopify store
	Append the generated document at JavaScript file

For each Shopify app
	create a Json structure
	Populate it with the normalized data from Shopify store
	Append the generated document at JavaScript file

Close all files

'''

apple_store_main_file = '../../datasets/Apple/AppleStore.csv'
apple_store_description_file = '../../datasets/Apple/appleStore_description.csv'

app_file_1 = pd.read_csv(apple_store_main_file, sep=',', quotechar='"', encoding='utf8')
app_file_2 = pd.read_csv(apple_store_description_file, sep=',', quotechar='"', encoding='utf8')

for i, j in app_file_1.iterrows():
	print(i)
	print(j)
	print()