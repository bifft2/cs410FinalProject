import os
from os import path, listdir
from os.path import isfile, join
import json as simplejson
import pprint
import csv

all_data = {}
pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "data/metadata/"
abs_file_path = os.path.join(script_dir, rel_path)

for f in listdir(abs_file_path):
	if isfile(join(abs_file_path, f)):
		current_object = {}
		file_name_pieces = f.split(".")
		metadata = open(join(abs_file_path, f)).read()
		data = simplejson.loads(metadata)
		restaurant_id = file_name_pieces[0]
		current_object["metadata"] = data
		current_object["similar_restaurants"] = []
		current_object["keywords"] = []
		current_object["reviews"] = []
		all_data[restaurant_id] = current_object

rel_path = "data/reviews/"
abs_file_path = os.path.join(script_dir, rel_path)
for f in listdir(abs_file_path):
	if isfile(join(abs_file_path, f)):
		sentiment_object = {}
		sentiment_object["positive_probability"] = 0
		sentiment_object["negative_probability"] = 0
		sentiment_object["neutral_probability"] = 0
		sentiment_object["label"] = ""

		file_name_pieces = f.split(";")
		restaurant_id = file_name_pieces[0]
		reviewer_id = file_name_pieces[1].split(".")[0]
		review_object = {}
		review_object["reviewer_id"] = reviewer_id
		review_object["sentiment"] = sentiment_object

		with open(join(abs_file_path, f), 'r') as myfile:
			data = myfile.read().replace('\n', '')
    	review_object["review"] = data
    	all_data[restaurant_id]["reviews"].append(review_object)

rel_path = "data/stars/"
abs_file_path = os.path.join(script_dir, rel_path)
for f in listdir(abs_file_path):
	if isfile(join(abs_file_path, f)):
		file_name_pieces = f.split(";")
		restaurant_id = file_name_pieces[0]
		reviewer_id = file_name_pieces[1].split(".")[0]

		with open(join(abs_file_path, f), 'r') as myfile:
			data = myfile.read().replace('\n', '')
		data = int(data)

		if restaurant_id in all_data:
			for review in all_data[restaurant_id]["reviews"]:
				if review["reviewer_id"] == reviewer_id:
					review["stars"] = data

rel_path = "data/summary_reviews.csv"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path, 'rb') as csvfile:
	summary_review_reader = csv.reader(csvfile, delimiter=',')
	for row in summary_review_reader:
		restaurant_id = row[0]
		if restaurant_id in all_data:
			all_data[restaurant_id]["review_summary"] = row[1]

dataFile = open("output.json", "w")

dataFile.write(simplejson.dumps(all_data, indent=4, sort_keys=True))
dataFile.close()
