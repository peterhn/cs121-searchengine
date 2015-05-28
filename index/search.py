#!/usr/bin/env python3
import json
import os

FILE_DOC_IDS = "./docIds.txt"
FILE_INVERTED_INDEX = "./invertedIndex.txt"
FILE_TERM_IDS = "./termIds.txt"
FILE_DUMP = "./FileDump/"


def _input(msg):

    # Uncomment the call to raw_input if you are using python2.
    # Also change the hashbang from python3 to python2

    # return raw_input(msg)
    return input(msg)

def parseInvertedIndex():
    # The inverted index is of the format
    # < int, <int, int> >
    # Where the key is the index of the term itself,
    # and the value is another mapping of
    # page names as keys tied to the frequency of occurence as values
    invertedIndex = {}


    # Open the invertedIndex file
    indexFile = open(FILE_INVERTED_INDEX, "r")
    # Read each line and parse it into the invertedIndex
    for line in indexFile:
        # line is the docId followed by a space and then a list of termIds
        data = line.split(" ")
        docId = int(float(data[0].strip()))
        terms = data[2:]

        # Create the key to dict mapping
        invertedIndex[docId] = {}

        for term in terms:
            t = int(float(term.strip()))
            if t in invertedIndex[docId]:
                invertedIndex[docId][t] += 1
            else:
                invertedIndex[docId][t] = 1

    indexFile.close()
    return invertedIndex;

def parseTermIds():

    # TermIds have the string term as the key, followed by the ID as an int
    termIds = {}

    termFile = open(FILE_TERM_IDS, "r")
    lines = termFile.readlines()[1:]
    for line in lines:
        data = line.split(" ")
        termId = int(float(data[0].strip()))
        term = data[1].strip()

        termIds[term] = termId

    return termIds

def parseDocs():
    docTexts = {}
    for fn in os.listdir(FILE_DUMP):
        try:
            with open(FILE_DUMP + fn) as data_file:
                data = json.load(data_file)
                docId = int(data["id"])
                text = str(data["text"]).lower()
                docTexts[docId] = text
        except ValueError:
            print('No valid JSON')
    return docTexts

def parseDocIds():

    # TermIds have the int ID as the key, followed by the string term as val
    docIds = {}

    docFile = open(FILE_DOC_IDS, "r")
    lines = docFile.readlines()[1:]
    for line in lines:
        data = line.split(" ")
        docId = int(float(data[0].strip()))
        doc = data[1].strip()

        docIds[docId] = doc

    return docIds

def handleSearchQuery(query, termIds, docIds, index, docTexts):
    # Searches for the query in the index

    # ONLY HANDLES SINGLE WORDS AT THE MOMENT
    # First get the term number from the query

    seenDocIds = []
    relevantDocIds = {}
    search = query.split()
    for word in search:
        if word not in termIds:
            print("Failed to find " + word + " in list of terms")
        else:
            termId = termIds[word]
            pages = index[termId]
            genexp = ((k, pages[k]) for k in sorted(pages, key=pages.get, reverse=True))

            for k, v in genexp:
                # k is docId
                # v is frequency of occurance (will be used to calculate relevance)
                if k not in seenDocIds:
                    seenDocIds.append(k)
                if k in seenDocIds:
                    #print("seen", k)
                    if k in relevantDocIds:
                        #print("words")
                        relevantDocIds[k] = relevantDocIds[k] + v
                    else:
                        relevantDocIds[k] = v

    print("The term: \"" + query +"\" occurs in the following documents...")
    for k in relevantDocIds:
        docText = docTexts[k]
        exactQueryCount = docText.count(query)
        relevantDocIds[k] = relevantDocIds[k] + (exactQueryCount * 100)

    sortedResults  = ((k, relevantDocIds[k]) for k in sorted(relevantDocIds, key=relevantDocIds.get, reverse=True)[:5])
    for k,v in sortedResults:
        print("\t",k, docIds[k], "\tRelevance Score: ", v)
        #print("\t", docIds[docId], "\tOccurs: ", v, "times")




def main():
    ''' The main function'''

    DEBUG = False

    # O(n^2)
    #  TODO Make this faster
    print('Building index...')
    index = parseInvertedIndex()
    if DEBUG or False:
        for term in index:
            print(term, index[term])

    # O(n)
    print('Building termIds...')
    termIds = parseTermIds()
    if DEBUG or False:
        for term in termIds:
            print(term, termIds[term])

    # O(n)
    print('Building docIds...')
    docIds = parseDocIds()
    if DEBUG or False:
        for term in docIds:
            print(term, docIds[term])

    # O(n)
    print('Building docTexts...')
    docTexts = parseDocs()
    if DEBUG or False:
        for docId in docTexts:
            print(docId, docTexts[docId])

    query = _input("Enter query: ").strip().lower()
    while query != "":
        # O(n)
        handleSearchQuery(query, termIds, docIds, index, docTexts)
        query = _input("Enter query: ").strip().lower()



if __name__ == "__main__":
    main()
