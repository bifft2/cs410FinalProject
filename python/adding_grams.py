import json
import csv

with open("out_with_sentiment.json") as fin:
    data = json.load(fin)
for r_id in data:
    data[r_id]["keywords"] = {}
with open('unigram_keywords.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        r_id = row[0]
        unigrams = []
        for i in range(1, len(row)):
            unigrams.append(row[i])
        data[r_id]["keywords"]["unigrams"] = unigrams
with open('bigram_keywords.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        r_id = row[0]
        bigrams = []
        for i in range(1, len(row)):
            bigrams.append(row[i])
        data[r_id]["keywords"]["bigrams"] = bigrams
with open('out_with_keywords.json', 'w') as outfile:
    json.dump(data, outfile)