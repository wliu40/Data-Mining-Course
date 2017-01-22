#import re
'''
We have record of the spam emails, using bloom filter algorithm, now
given a data stream contains many email usernames, we need to recognize 
whether it is in the spam emails set or not, give the false_positive analysis based
on the number of hash functions.
'''
import hashlib
import random

#Open files
with open('listed_username_30.txt', 'r') as myfile1:
    spam_emails_txt = myfile1.read()
    
with open('listed_username_365.txt', 'r') as myfile2:
    stream = myfile2.read()
        

spam_emails_set = spam_emails_txt.split()
#print len(spam_emails_set)

stream_emails_set = stream.split()
#print len(stream_emails_set)



class Bloom:
    def __init__(self, m, k, hash_fun):
        """
        m: size of the vector (size of the targets)
        k: number of hash functions to use
        hash_fun: the hash function which hashs a string to a random number
        in the range of [0, m-1]
        vector: we use a int list to mimic the bit-array, initiate to all zeros
        """
        self.m = m
        self.k = k
        self.hash_fun = hash_fun
        self.vector = [0]*m
        self.data = {}
        self.false_positive = 0
        
    def insert(self, key, value):
        #save this key to the spam emails collection
        self.data[key] = value
        #use the k hash functions, set the vector[hash value] to 1
        for i in range(self.k):
            self.vector[self.hash_fun(key+str(i)) % self.m] = 1
            
    def contains(self, key):
        """ check if a key (string) should be filtered or not,
            if for all the k hash functions, the vector has a 0 element
            then this key must be a spam,
            otherwise, it could be contained in the validated email set
        """
        for i in range(self.k):
            if self.vector[self.hash_fun(key+str(i)) % self.m] == 0:
                return False
        return True
        
    def check(self, key):
        if self.contains(key):
            try:
                return self.data[key]
            except KeyError:
                self.false_positive += 1



        '''if key not in self.spam_emails:
            self.false_positive += 1'''

 
def my_hash(x):
    h = hashlib.sha256(x) # use sha256 just for this example
    return int(h.hexdigest(),base=16) 
      
'''generate random strings using the characters in chars, the length is n'''
def rand_data(n, chars):
    return ''.join(random.choice(chars) for i in range(n))

    
 
#rand_keys = [rand_data(10,'abcde') for i in range(1000)]
#rand_keys2 = rand_keys + [rand_data(10,'fghil') for i in range(1000)]

def bloomTest(target_string_set, dart_string_set, k):
    bloom = Bloom(10*len(target_string_set), k, my_hash)
    for i in target_string_set:
        bloom.insert(i, 'data')
    for j in dart_string_set:
        bloom.check(j)
    #print bloom.false_positive
    #print len(dart_string_set)
    return float(bloom.false_positive)/len(dart_string_set)*100
 
'''
#print bloomTest(rand_keys,rand_keys2,1)
bloomTest(spam_emails_set,stream_emails_set,1)
'''
k = range(1,20)

percentage = [bloomTest(spam_emails_set,stream_emails_set,kk) for kk in k] # k is varying

# plotting the result of the test
from pylab import plot,show,xlabel,ylabel
plot(k,percentage,'--ob',alpha=.7)
ylabel('false positive %')
xlabel('k')
show()

