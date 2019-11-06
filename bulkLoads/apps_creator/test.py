import os

script_file = './test.js'

if (os.path.isfile(script_file)):
	os.remove(script_file)

script = open(script_file, "w+")

script.write('db.AppsCollection.insertMany([')


document = '{"id": item,"categories": [{"name": item}],"apps_price_plans": [{"currencies:" [{"currency": item,"price": item}]}],"age_rating": item,"name": item,"rating": item,"apple_apps":{"app_description": item,"version": item,"n_of_supported_devices":item,"n_of_reviews": item,"n_of_ipad_urls": item,"n_of_available_languages": item,"belongs_to_volume_purchase_program": item,"rating_curr_version": item,"n_of_rating_curr_version": item,"size": item}'

script.write(document)
script.write('])')