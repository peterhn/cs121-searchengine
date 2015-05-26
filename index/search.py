#!/usr/bin/env python3

FILE_DOC_IDS = "./docIds.txt"
FILE_INVERTED_INDEX = "./invertedIndex.txt"
FILE_TERM_IDS = "./termIds.txt"

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
        termId = int(data[0].strip())
        term = data[1].strip()

        termIds[term] = termId

    return termIds

def main():
    ''' The main function'''

    DEBUG = False

    index = parseInvertedIndex()
    if DEBUG or False:
        for term in index:
            print(term, index[term])

    termIds = parseTermIds()
    if DEBUG or True:
        for term in termIds:
            print(term, termIds[term])

    query = input("Enter query: ").strip().lower()
    while query != "":
        query = input("Enter query: ").strip().lower()



if __name__ == "__main__":
    main()
