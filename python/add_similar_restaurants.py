import json as simplejson
import csv

with open("out_with_photos_codebeautify.json") as json_file:
    json_data = simplejson.load(json_file)

with open('similar.csv', 'rb') as csvfile:
	similar_review_reader = csv.reader(csvfile, delimiter=',')
	for row in similar_review_reader:
		restaurant_id = row[0]
		similar_list = row[1:11]
		if restaurant_id in json_data:
			json_data[restaurant_id]["similar_restaurants"] = similar_list

dataFile = open("output.json", "w")

dataFile.write(simplejson.dumps(json_data, indent=4, sort_keys=True))
dataFile.close()