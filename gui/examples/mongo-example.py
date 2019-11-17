from pymongo import MongoClient

# Connect with the portnumber and host
client = MongoClient(host=['localhost:27017'])

# Access database
db = client['database']

# Access collection of the database
collection_app = db['apps']

rec = {
	"id" : 281656475,
	"categories" : [ "games" ],
	"apps_price_plans" : [ {"currencies" : [{"currency" : "USD" , "price" : 399}]} ],
	"age_rating" : "4",
	"name" : "pacman premium",
	"rating" : 40,
	"apple_apps" : {
		"app_description" : "save 20 now only 399 for a limited timeone of the most popular video games in arcade history2015 world video game hall of fame inducteewho can forget the countless hours and quarters spent outrunning pesky ghosts and chompin on dots now you can have the same arcade excitement on your mobile devices guide pacman through the mazes with easy swipe controls a mfi controller or kick it old school with the onscreen joystickeat all of the dots to advance to the next stage go for high scores and higher levels gain an extra life at 10000 points gobble power pellets to weaken ghosts temporarily and eat them up before they change back avoid blinky the leader of the ghosts and his fellow ghosts pinky inky and clyde or you will lose a life its game over when you lose all your lives9 new mazes includedthe game includes 9 new mazes in addition to the pixel for pixel recreation of the classic original maze challenge your skill to beat them all we are constantly updating the game with new maze packs that you can buy to complete your pacman collectionhints and tipsinsider protips and hints are being made available for the first time ingame use these to help you become a pacman championfeatures new tournaments new visual hints and protips new mazes for all new challenges play an arcade perfect port of classic pacman two different control modes three game difficulties including the original 1980 arcade game retina display support mfi controller support",
		"version" : "635",
		"n_of_supported_devices" : 38,
		"n_of_reviews" : 21292,
		"n_of_ipad_urls" : 5,
		"n_of_available_languages" : 10,
		"belongs_to_volume_purchase_program" : 1,
		"rating_curr_version" : 45,
		"n_of_rating_curr_version" : 26,
		"size" : 100788224
	}
}

# inserting the data in the database
rec = collection_app.insert_one(rec)

result = collection_app.find({"id" : 281656475})

print("Print ID:", result[0]["id"])
print(result[0])