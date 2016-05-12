import json
import os
import operator
import csv
from pprint import pprint

def form_dictionary():
    file_list = os.listdir("metadata")
    meta_dict = {}
    for f in file_list:
        fname_split = f.split('.')
        uuid = fname_split[0]
        with open("".join(["metadata/", f]), 'r') as data_file:
            metadata = json.load(data_file)
            meta_dict[uuid] = metadata
    return meta_dict

def form_unigram_bigram_dict():
    uni_bi_dict = {}
    with open('unigram_keywords.csv', 'r') as unifile:
        unireader = csv.reader(unifile, delimiter=',')
        for row in unireader:
            uuid = row[0]
            uni_bi_dict[uuid] = {"unigram":row[1:]}
    with open('bigram_keywords.csv', 'r') as bifile:
        bireader = csv.reader(bifile, delimiter=',')
        for row in bireader:
            uuid = row[0]
            uni_bi_dict[uuid]["bigram"] = row[1:]
    return uni_bi_dict

def two_sim(meta_dict, uni_bi_dict, uu1, uu2):
    sim = 0
    #compare categories - weight this heaviy
    #print uu1
    #print uu2
    cat1 = meta_dict[uu1]["categories"]
    cat2 = meta_dict[uu2]["categories"]
    cat_set1 = set(cat1)
    cat_set2 = set(cat2)
    intersect_l = list(cat_set1 & cat_set2)
    union_l = list(cat_set1 | cat_set2)
    j_index = float(len(intersect_l))/len(union_l)
    sim += 2*j_index
    #compare attributes - ambience booleans
    if "Ambience" in meta_dict[uu1]["attributes"] and "Ambience" in meta_dict[uu2]["attributes"]:
        amb1 = meta_dict[uu1]["attributes"]["Ambience"]
        amb2 = meta_dict[uu2]["attributes"]["Ambience"]
        amb_cat_count = len(amb1)
        amb_match = 0
        for ambkey in amb1:
            if ambkey in amb2:
                val1 = amb1[ambkey]
                val2 = amb2[ambkey]
                if val1 == val2:
                    amb_match += 1
        sim += (float(amb_match)/amb_cat_count)
    #compare attributes - good for booleans
    if "Good For" in meta_dict[uu1]["attributes"] and "Good For" in meta_dict[uu2]["attributes"]:
        gf1 = meta_dict[uu1]["attributes"]["Good For"]
        gf2 = meta_dict[uu2]["attributes"]["Good For"]
        gf_cat_count = len(gf1)
        gf_match = 0
        for gfkey in gf1:
            if gfkey in gf2:
                val1 = gf1[gfkey]
                val2 = gf2[gfkey]
                if val1 == val2:
                    gf_match += 1
        sim += (float(gf_match)/gf_cat_count)
    #compare hours - amount of overlap?
    hours1 = meta_dict[uu1]["hours"]
    hours2 = meta_dict[uu1]["hours"]
    #pull in keywords too
    uni1 = uni_bi_dict[uu1]["unigram"]
    uni2 = uni_bi_dict[uu2]["unigram"]
    bi1 = uni_bi_dict[uu1]["bigram"]
    bi2 = uni_bi_dict[uu2]["bigram"]
    #compare unigrams
    uni_set1 = set(uni1)
    uni_set2 = set(uni2)
    intersect_u = list(uni_set1 & uni_set2)
    union_u = list(uni_set1 | uni_set2)
    j_index_u = float(len(intersect_u))/len(union_u)
    sim += j_index_u
    #compare bigrams
    bi_set1 = set(bi1)
    bi_set2 = set(bi2)
    intersect_b = list(bi_set1 & bi_set2)
    union_b = list(bi_set1 | bi_set2)
    j_index_b = float(len(intersect_b))/len(union_b)
    sim += 2*j_index_b
    return sim

def compute_sim():
    meta_dict = form_dictionary()
    uni_bi_dict = form_unigram_bigram_dict()
    #loop through uuids
    with open('similar.csv', 'w') as simfile:
        simwriter = csv.writer(simfile, delimiter=',')
        for uuid in meta_dict:
            #find 10? most similar
            sim_dict = {}
            for uuid_comp in meta_dict:
                if uuid_comp != uuid:
                    sim = two_sim(meta_dict, uni_bi_dict, uuid, uuid_comp)
                    sim_dict[uuid_comp] = sim
            sorted_uuids = sorted(sim_dict.items(), key=lambda x: x[1],
                    reverse=True)
            selected_uuids = [x[0] for x in sorted_uuids[:10]]
            row_list = [uuid]
            for u in selected_uuids:
                row_list.append(u)
            #print uuid
            #for u in selected_uuids:
            #    print u, sim_dict[u]
            simwriter.writerow(row_list)

if __name__=="__main__":
    compute_sim()
