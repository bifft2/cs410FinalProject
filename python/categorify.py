import json
from pprint import pprint
with open("final_output.json") as fin:
    data = json.load(fin)
categories = {}
for datum in data:
    for category in data[datum]["metadata"]["categories"]:
        category = category.replace("/", "-")
        category = category.replace(" ", "_")
        category = category.replace("&", "and")
        if category not in categories:
            categories[category] = []
        categories[category].append(datum)
pprint(len(categories))
for category in categories:
    with open("data/categories/"+category+".json","w") as fout:
        category_out = {}
        for restaurant in categories[category]:
            category_out[restaurant] = data[restaurant]
        json.dump(category_out, fout,  indent=4, sort_keys=True)