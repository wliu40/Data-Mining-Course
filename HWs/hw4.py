
import re
import numpy as np
from numpy import array
from collections import Counter
from scipy.cluster.vq import kmeans,vq, whiten
from sklearn.cluster import KMeans

#Open files
with open('foods.txt', 'r') as myfile:
    s = myfile.read()    
with open('stop_words.txt', 'r') as myfile2:
    stop_words_string = myfile2.read()

#initiate two index locator
start, end = 0, 0

#strings to locate the review string
str_review = 'review/text:'
str_product = 'product/productId'
rx = re.compile('\W+')

#create a tuple which include all the stop words 
#from the stop words txt file
stop_words_tuple = tuple(rx.sub(' ',stop_words_string).strip().split())
#we will merge all reviews into one single string to find the frequent words
all_reviews_string = ''
#also, we need a review list to identify each review
#the elements in the review_list will be dictionary with word:occurence time
review_list = []
#the last review is special, we need its index to locate it
last_review_pos = s.rindex(str_review)
flag = 1
while flag is 1:
    start = s.index(str_review, end+len(str_product))
    if(start < last_review_pos):
        end = s.index(str_product, start+len(str_review))
    else:
        end = -1
        flag = 0
    #catch the reviews one by one
    review = s[start+len(str_review):end]
    
    #clean the review, get rid of the punctuations and other marks
    clean_review = rx.sub(' ', review).strip()
    
    #add each lowcase review to the all_review_string
    all_reviews_string += clean_review.lower()
    #record each word and its occurence
    
    dic = dict(Counter(clean_review.lower().split()))
    #pop all the common words
    for i in stop_words_tuple:
        dic.pop(i, None)
    
    #add each dictionary to review_list
    review_list.append(dic)
#how many reviews are there in the foods.txt?    
print 'how many reviews? :' + str(len(review_list))

#all_reviews_string +=  re.sub('[\[\]/{}<>()\"\'@.,;!?*$~]+-%', '', s[s.rindex(s1)+len(s1):-1].lower())
#get the words and their count number in the whole review string, save this to dictionary
all_words_dic = Counter(all_reviews_string.split())
#clean the all review string
for i in stop_words_tuple:
    all_words_dic.pop(i, None)

#sort the dictionary by the value
frequent_words = sorted(all_words_dic.items(),key=lambda x: x[1], reverse = True)
#print the first 500 most frequent words and their count number
print 'The 500 most frequent words and their count is:'
print frequent_words[0:500]
#save those 500 words in a list
frequent_words_list = []
for i in range(0,500):
    frequent_words_list.append(frequent_words[i][0])
#vectorize each review by its representing dictionary and the frequent words list
feathers = []
for i in range(len(review_list)):
    row = []
    for j in range(0,500):
        row.append( (review_list[i].get(frequent_words_list[j], 0)) )    
    feathers.append(row)

feathers = np.array(feathers)

#run k-means clustering, cluster the data to 10 clusters
kmeans = KMeans(n_clusters=10, random_state=0).fit(feathers)

#there are 10 centers for 10 clusters, which is 500 dimension vector
for center in kmeans.cluster_centers_:    
    #print each center vector
    #print center
    
    #for each center, sort the center, return its indices for the sorted elements, there
    #should be 500 indices for each center
    order = [i[0] for i in sorted(enumerate(center), key=lambda x:x[1], reverse = True)]

    #the top five feathers and their values
    center_feature = []
    feature_value = []
    for j in range(0, 5):
        center_feature.append(frequent_words_list[order[j]])
        feature_value.append(center[order[j]])
    print '' 
    print '----------------------------' 
    print center_feature
    print feature_value
