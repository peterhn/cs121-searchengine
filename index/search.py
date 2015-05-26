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
        termId = int(float(data[0].strip()))
        term = data[1].strip()

        termIds[term] = termId

    return termIds

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

def handleSearchQuery(query, termIds, docIds, index):
    # Searches for the query in the index

    # ONLY HANDLES SINGLE WORDS AT THE MOMENT
    # First get the term number from the query
    if query not in termIds:
        print("Failed to find " + query + " in list of terms")
    else:
        termId = termIds[query]
        pages = index[termId]
        genexp = ((k, pages[k]) for k in sorted(pages, key=pages.get, reverse=True)[:5])

        print("The term: \"" + query +"\" occurs in the following documents...")
        for k, v in genexp:
            # k is docId
            # v is frequency of occurance
            print("\t", docIds[k], "\tOccurs:", v, "times")



def main():
    ''' The main function'''

    DEBUG = False

    index = parseInvertedIndex()
    if DEBUG or False:
        for term in index:
            print(term, index[term])

    termIds = parseTermIds()
    if DEBUG or False:
        for term in termIds:
            print(term, termIds[term])

    docIds = parseDocIds()
    if DEBUG or False:
        for term in docIds:
            print(term, docIds[term])

    query = input("Enter query: ").strip().lower()
    while query != "":
        handleSearchQuery(query, termIds, docIds, index)
        query = input("Enter query: ").strip().lower()



if __name__ == "__main__":
    main()
