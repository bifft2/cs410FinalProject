import os
import csv

def run_filter_freqs():
    #os.chdir('reviews')
    file_list = os.listdir('all')
    with open('unigram_keywords.csv', 'w') as unifile:
        uniwriter = csv.writer(unifile, delimiter=',')
        for f in file_list:
            fname_split = f.split('.')
            if (len(fname_split)==4) and fname_split[2]=="1":
                #print f
                with open("".join(["all/", f]), 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=' ')
                    save_words = [fname_split[0]]
                    for row in reader:
                        word = row[0]
                        if (len(save_words) == 11):
                            break
                        if (len(word) != 1) and (word[0] != '\''):
                            save_words.append(word)
                    uniwriter.writerow(save_words)
    with open('bigram_keywords.csv', 'w') as bifile:
        biwriter = csv.writer(bifile, delimiter=',')
        for f in file_list:
            fname_split = f.split('.')
            if (len(fname_split)==4) and fname_split[2]=="2":
                #print f
                with open("".join(["all/", f]), 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=' ')
                    save_words = [fname_split[0]]
                    for row in reader:
                        word_pair = row[0]
                        split_word_pair = word_pair.split("_")
                        word1 = split_word_pair[0]
                        word2 = split_word_pair[1]
                        if (len(save_words) == 11):
                            break
                        if (len(word1) != 1) and (word1[0] != '\''):
                            if (len(word2) != 1) and (word2[0] != '\''):
                                save_words.append(word_pair)
                    biwriter.writerow(save_words)

if __name__ == "__main__":
    run_filter_freqs()
