import json
import os
import operator
import csv
from itertools import product
from collections import defaultdict
from pprint import pprint
from numpy import arange

def form_truth_table():
    sim_truth_dict = defaultdict(list)
    with open('sim.csv', 'r') as simfile:
        reader = csv.reader(simfile, delimiter=',')
        for row in reader:
            uuid1 = row[0]
            if uuid1 not in sim_truth_dict:
                sim_truth_dict[uuid1] = []
            for uuid2 in row[1:]:
                sim_truth_dict[uuid1].append(uuid2)
                sim_truth_dict[uuid2].append(uuid1)
    return sim_truth_dict

def form_dictionary():
    file_list = os.listdir("training/training_metadata")
    meta_dict = {}
    for f in file_list:
        fname_split = f.split('.')
        uuid = fname_split[0]
        with open("".join(["training/training_metadata/", f]), 'r') as data_file:
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

def two_sim(meta_dict, uni_bi_dict, uu1, uu2, c, a, g, u_var, b):
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
    sim += c*j_index
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
        sim += a*(float(amb_match)/amb_cat_count)
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
        sim += g*(float(gf_match)/gf_cat_count)
    #compare hours - no
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
    #print type(u_var), type(j_index_u), u_var
    sim += u_var*j_index_u
    #compare bigrams
    bi_set1 = set(bi1)
    bi_set2 = set(bi2)
    intersect_b = list(bi_set1 & bi_set2)
    union_b = list(bi_set1 | bi_set2)
    j_index_b = float(len(intersect_b))/len(union_b)
    sim += b*j_index_b
    return sim

def compute_sim(c, a, g, u_var, b):
    meta_dict = form_dictionary()
    uni_bi_dict = form_unigram_bigram_dict()
    found_results_dict = {}
    #loop through uuids
    for uuid in meta_dict:
        #find 10? most similar
        sim_dict = {}
        for uuid_comp in meta_dict:
            if uuid_comp != uuid:
                sim = two_sim(meta_dict, uni_bi_dict, uuid, uuid_comp, c, a, g, u_var, b)
                sim_dict[uuid_comp] = sim
        sorted_uuids = sorted(sim_dict.items(), key=lambda x: x[1],
                reverse=True)
        selected_uuids = [x[0] for x in sorted_uuids[:10]]
        row_list = [uuid]
        for u in selected_uuids:
            row_list.append(u)
        found_results_dict[uuid] = selected_uuids
    return found_results_dict

def calc_precision_recall(truth, found):
    relevant_retrieved = 0
    relevant_rejected = 0
    irrelevant_retrieved = 0
    for uuid in truth:
        for relevant in truth[uuid]:
            if relevant in found[uuid]:
                relevant_retrieved += 1
            else:
                relevant_rejected += 1
        for retrieved in found[uuid]:
            if retrieved not in truth[uuid]:
                irrelevant_retrieved += 1
    precision = float(relevant_retrieved)/(relevant_retrieved + irrelevant_retrieved)
    recall = float(relevant_retrieved)/(relevant_retrieved + relevant_rejected)
    return precision, recall

def calc_score(sim_truth, c, a, g, u, b):
    found_results = compute_sim(c, a, g, u, b)
    precision, recall = calc_precision_recall(sim_truth, found_results)
    f1 = (2*precision*recall)/(precision + recall)
    return f1

if __name__=="__main__":
    sim_truth_dict = form_truth_table()
    uni_weights = [i for i in arange(0.5, 3.0, 0.50)]
    bi_weights = [i for i in arange(0.5, 3.0, 0.50)]
    cat_weights = [i for i in arange(0.5, 3.0, 0.50)]
    amb_weights = [i for i in arange(0.5, 3.0, 0.50)]
    gf_weights = [i for i in arange(0.5, 3.0, 0.50)]
    weight_prod = list(product(cat_weights, amb_weights, gf_weights, uni_weights, bi_weights))
    c_best = 25
    a_best = 25
    g_best = 25
    u_best = 25
    b_best = 25
    best_score = 0
    for w in weight_prod:
        c = w[0]
        a = w[1]
        g = w[2]
        u = w[3]
        b = w[4]
        #print c, a, g, u, b
        score = calc_score(sim_truth_dict, c, a, g, u, b)
        print c, a, g, u, b, score
        if (score > best_score):
            best_score = score
            c_best = c
            a_best = a
            g_best = g
            u_best = u
            b_best = b
    print "c_best", c_best
    print "a_best", a_best
    print "g_best", g_best
    print "u_best", u_best
    print "b_best", b_best
    #compute_sim()
