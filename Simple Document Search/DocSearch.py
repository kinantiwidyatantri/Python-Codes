import numpy as np
import math


def readfilesdocs(namefile): #funtion to read the docs.txt input and put it in 
    with open(namefile, 'r') as f:
        id = [(x.strip('\n'), i) for i, x in enumerate(f.readlines(), 1)]
    
    return id

def readfilesqueries(queriesname): #funtion to read the queries.txt input
    with open(queriesname, 'r') as f:
        querieslist  = [x.strip('\n') for x in f.readlines()]
        
    return querieslist

def makedictionary(namefile): # funtion to build the dictionary
    mydictionary = []   #the dictionary  
   
    with open(namefile,'r') as file: #read the .txt file word by word
        for line in file:
            for word in line.split():
                mydictionary.append(word) #append the word to mydictionary to build dictionary
                    
    mydictionary = list(dict.fromkeys(mydictionary)) #remove duplicate

    return mydictionary 

def makeinvertedindex(dictionary, relateddocs): #make inverted index for finding the relevant document
    index = {} #create dictionary for index

    for word in dictionary: #give index to elements
        index[word] = []

    for doc in relateddocs: # taking elements in the dpcs.txt file
        for word in doc[0].split():
            if word in index and doc[1] not in index[word]:
                index[word].append(doc[1])
   
    return index


def generatevector(docsline, dictionary): # generating vector for the calculation
    vector = np.zeros(len(dictionary)) #makes vector with the length of the dcitionary

    for i, word in enumerate(dictionary):
        vector[i] = docsline.count(word)

    return vector


def calc_angle(x,y): #calculating the angle
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos_theta = np.dot(x, y) / (norm_x * norm_y)
    theta = math.degrees(math.acos(cos_theta))

    
    return theta
    


def main(docsname, queriesname): # executing the function
    quelist = readfilesqueries(queriesname) #read the queries.txt
    wordslist = readfilesdocs(docsname) #read the docs.txt
    dict = makedictionary(docsname) #call the dictionary function
    invertedindex = makeinvertedindex(dict, wordslist) #call inverted index function

    
    print("Words in dictionary:", len(dict))

    
    for words in quelist: #itirate through the queries words
        print(f"Query: {words}")
        vector_queries = generatevector(words, dict) #generate vector for each query
        word_list= []
        
        for a in words.split(): # find the relevant documents using inverted index
            if a in invertedindex:
                x = invertedindex[a]
                word_list.append(set(x))

        relevantdocs = set.intersection(*word_list) 
        print(f"Relevant documents: {relevantdocs}")

        angles = {} # calculate the angle and sort it from the smallest
        for sentence in wordslist:
            if sentence[1] in relevantdocs:
                word = sentence[0].split()
                vector_docs = generatevector(word,dict) #generate vector for each document in docs.txt
                a = calc_angle(vector_queries, vector_docs)
                angles[sentence[1]] = a

        sorted_angle = sorted(angles.items(), key=lambda item: item[1]) #sort the angles
        for x in sorted_angle:
            print(f"{x[0]} {x[1] : .5f}")
        


main("docs.txt","queries.txt")