import json
import csv
import urllib.request
from yelpapi import YelpAPI
from pprint import pprint
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import rauth

consumer_key="MuYtDM8NHK-Llc_m7HmTHw"
consumer_secret="fH7NYxSTt0xBI8bv1PpDXxPGE0M"
token="VtuaK3usj3lWbD8fs08_c-sLAjxa5EQj"
token_secret="YoSJ7t03UlvDaUc_6wsTfOl6JmI"

session = rauth.OAuth1Session(
consumer_key = consumer_key
,consumer_secret = consumer_secret
,access_token = token
,access_token_secret = token_secret)

with open("out_with_keywords.json") as fin:
    data = json.load(fin)
bad_ids = []
print(len(data))
for r_id in data:
    actual_name = data[r_id]["metadata"]["name"]
    actual_address = data[r_id]["metadata"]["full_address"].split("\n")
    params = {}
    params["ll"] = "{},{}".format(str(data[r_id]["metadata"]["latitude"]),str(data[r_id]["metadata"]["longitude"]))
    params["radius_filter"] = "2000"
    params["term"] = actual_name
    request = session.get("https://api.yelp.com/v2/search/", params=params)
    result = request.json()
    done = False
    for business in result["businesses"]:
        if business["name"] == actual_name and actual_address == business["location"]["display_address"]:
            print(business)
            exit()
            if "image_url" in business:
                data[r_id]["metadata"]["photo"] = business["image_url"]
                print(business["image_url"])
            done = True
    if done is False:
        bad_ids.append(r_id)


session.close()
for id in bad_ids:
    del data[id]
print(len(data))

with open('out_with_photos.json', 'w') as outfile:
    json.dump(data, outfile)