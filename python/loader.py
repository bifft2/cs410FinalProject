import json

def main():
    business_data = {}
    lines = []
    with open("yelp_academic_dataset_business.json") as businesses:
        lines = businesses.readlines()
    for line in lines:
        data = json.loads(line)
        if "Restaurants" in data["categories"]:
        	if "Urbana" == data["city"] or "Champaign" == data["city"]:
        		business_id = data["business_id"]
        		business_data[business_id] = {"metadata": data, "reviews":[]}
        		with open("data/metadata/"+business_id+".txt", "w") as meta_file:
            			json.dump(business_data[business_id]["metadata"], meta_file)
    print(len(business_data))
    
    i = 0
    with open("yelp_academic_dataset_review.json") as review_doc:
        for review in review_doc:
            review_data = json.loads(review)
            business_id = review_data["business_id"]
            if i%10000 == 0:
			print("review", i)
            if business_id in business_data.keys():
            	user_id = review_data["user_id"]
            	text = review_data["text"]
            	business_data[business_id]["reviews"].append(text)
            	with open("data/reviews/"+business_id+";"+user_id+".txt", "w") as review_file:
                	review_file.write(text.encode('ascii','ignore'))
            	stars = review_data["stars"]
            	with open("data/stars/"+business_id+";"+user_id+".txt", "w") as star_file:
                	star_file.write(str(stars).encode('ascii','ignore'))
            i+=1
    i = 0
    for business_id in business_data:
        if i % 10000 == 0:
            print("business", i)
        with open("data/all/"+business_id+".txt", "w") as all_file:
            all_file.write("\n".join(business_data[business_id]["reviews"]).encode('ascii','ignore'))
        i+=1

if __name__ == "__main__":main()
