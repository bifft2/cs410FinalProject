import json
import os
import operator
import csv
from pprint import pprint

def prompt_user():
    initial = raw_input("Please enter your first initial")
    name = initial.lower()
    u_id = 0
    if name == 'b':
        u_id = 1
    elif name == 'r':
        u_id = 2
    elif name == 'p':
        u_id = 3
    else:
        print "Invalid initial entered"
        return
    create_training(u_id)

def create_training(user):
    file_list = os.listdir('training_metadata')
    id_name_dict = {}
    for f in file_list:
        fname_split = f.split('.')
        uuid = fname_split[0]
        with open("".join(["training_metadata/", f]), 'r') as data_file:
            metadata = json.load(data_file)
            id_name_dict[uuid] = metadata["name"]
    #print id_name_dict
    with open('sim.csv', 'w') as simfile:
        writer = csv.writer(simfile, delimiter=',')
        alpha_id = sorted(list(id_name_dict))
        #print alpha_id
        start_i_list = [0, 8, 19]
        end_i_list = [8, 19, 45]
        start_index = start_i_list[user-1]
        end_index = end_i_list[user-1]
        for i in range(start_index, end_index):
            #print i
            similar_list = []
            name_list = []
            uuid1 = alpha_id[i]
            name1 = id_name_dict[uuid1]
            write_row = [uuid1]
            for j in range(i+1, 45):
                #print i, j
                uuid2 = alpha_id[j]
                name2 = id_name_dict[uuid2]
                similar = "x"
                while (similar != "0" and similar != "1"):
                    print "are {0} and {1} similar?".format(name1, name2)
                    similar = raw_input("1 for yes (similar), 0 for no")
                if similar == "1":
                    write_row.append(uuid2)
                    similar_list.append(uuid2)
                    name_list.append(name2)
            print name1, name_list
            #write_row.append(similar_list)
            writer.writerow(write_row)

if __name__=="__main__":
    prompt_user()
