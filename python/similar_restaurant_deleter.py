import json as simplejson

with open("final_output.json") as json_file:
    json_data = simplejson.load(json_file)


for restaurant_id in json_data:
	for current_restaurant_id in json_data[restaurant_id]["similar_restaurants"]:
		if current_restaurant_id in json_data.keys():
			continue
		else:
			print("deleting")
			json_data[restaurant_id]["similar_restaurants"].remove(current_restaurant_id)


dataFile = open("final_output.json", "w")

dataFile.write(simplejson.dumps(json_data, indent=4, sort_keys=True))
dataFile.close()