import os

def run_count_files():
    #os.chdir('reviews')
    review_file_list = os.listdir('reviews')
    sorted(review_file_list)
    #print review_file_list
    first_review = review_file_list[0]
    last_review = review_file_list[len(review_file_list)-1]
    first_num = int(first_review.split(";")[0])
    last_num = int(last_review.split(";")[0])
    num_to_count = {}
    for i in range(first_num, last_num+1):
        num_list = [f for f in review_file_list if (int(f.split(";")[0]) == i)]
        if num_list:
            num_to_count[i] = len(num_list)
    num_to_count_l = sorted(num_to_count, key=num_to_count.get, reverse=True)
    for i in range(0,10):
        print num_to_count_l[i], num_to_count[num_to_count_l[i]]

if __name__ == "__main__":
    run_count_files()
