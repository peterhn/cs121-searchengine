#!/usr/bin/env python3
import json
import os
import math

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

def parseDocData(docId):
    # The doc texts are ordered in the same way as the ids,
    # instead of opening all of them, just parse them on demand
    fn = FILE_DUMP + str(int(float(docId))) + ".txt"
    text = ""
    try:
        with open(fn) as data:
            jsonData = json.load(data)
            text = str(jsonData["text"]).lower()
    except ValueError:
        print("No valid JSON in file: ", fn)
    return text
    # for fn in os.listdir(FILE_DUMP):
    #     try:
    #         with open(FILE_DUMP + fn) as data_file:
    #             data = json.load(data_file)
    #             docId = int(data["id"])
    #             text = str(data["text"]).lower()
    #             docTexts[docId] = text
    #     except ValueError:
    #         print('No valid JSON')
    # return docTexts

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

# def handleSearchQuery(query, termIds, docIds, index, docTexts):
#     # Searches for the query in the index

#     # ONLY HANDLES SINGLE WORDS AT THE MOMENT
#     # First get the term number from the query

#     seenDocIds = []
#     relevantDocIds = {}
#     search = query.split()
#     for word in search:
#         if word not in termIds:
#             print("Failed to find " + word + " in list of terms")
#         else:
#             termId = termIds[word]
#             pages = index[termId]
#             genexp = ((k, pages[k]) for k in sorted(pages, key=pages.get, reverse=True))

#             for k, v in genexp:
#                 # k is docId
#                 # v is frequency of occurance (will be used to calculate relevance)

#                 # This is a waste of time as it will always evaluate to true,
#                 # EX
#                 # k = "foo"
#                 # if "foo" is not in seenDocIds, add it
#                 # foo will always be in seenDocIds as a result, it will always
#                 # be checked in the following if/else
#                 # As such, we should not need to check for k in seenDocIds

#                 # if k not in seenDocIds:
#                 #     seenDocIds.append(k)
#                 # if k in seenDocIds:
#                 # print("seen", k)

#                 if k in relevantDocIds:
#                     #print("words")
#                     relevantDocIds[k] += v
#                 else:
#                     relevantDocIds[k] = v

#     print("The term: \"" + query +"\" occurs in the following documents...")
#     for k in relevantDocIds:
#         docText = docTexts[k]
#         exactQueryCount = docText.count(query)
#         relevantDocIds[k] = relevantDocIds[k] + (exactQueryCount * 100)

#     sortedResults  = ((k, relevantDocIds[k]) for k in sorted(relevantDocIds, key=relevantDocIds.get, reverse=True)[:5])
#     for k,v in sortedResults:
#         print("\t",k, docIds[k], "\tRelevance Score: ", v)
#         #print("\t", docIds[docId], "\tOccurs: ", v, "times")

def booleanSearch(word, termIds, index):
    # Get the ID of the term
    termId = termIds[word]

    # Get the list of pages which contain the term somewhere
    pages = list(index[termId])

    return pages


def findTFIDF(termId, document, docIds, index):
    # Get the dict of pages which contain the term somewhere
    pages = index[termId]

    # Get the TF for the given term
    # TF = # of times t appears in doc / total # of terms in doc
    # Get the document in question
    if document in pages:
        docText = parseDocData(document)
        termCount = float(pages[document])
        docSize = float(len(docText.split()))
        tf = termCount / docSize

        # Get the IDF for the given term
        # IDF = total # of documents / number of documents that contain
        # the termId
        idf = math.log(float(len(docIds)) / float(len(pages)))

        # Compute the tf-idf
        return float(tf * idf)
    else:
        # Term was not in document
        return -1


def computeAllTFIDF(docs, termIds, docIds, index, search, weight):
    tfidfScores = {}
    for doc in docs:
        for word in search:
            termId = termIds[word]
            tfidf = findTFIDF(termId, doc, docIds, index)
            if tfidf != -1:

                # Put tfidf into map
                if doc not in tfidfScores:
                    # Write the tfidf score to the doc for the term
                    # Weigh the good doc scores more
                    # For now, just double them or whatever
                    tfidfScores[doc] = (tfidf * weight)
                else:
                    print("tfidf for docId:", doc, "is alread contained. Is this an error?")
                    score = tfidfScores[doc]
                    print("Old Score: ", score)
                    newScore = (tfidf * weight)
                    print("Averaging scores for new tfidf")
                    tfidfScores[doc] = float(score + newScore) / 2.0

    return tfidfScores

def computeScore(docs, termIds, docIds, index, search, weight):
    score = {}

    # TODO(peter or francis) Cosine Vector evaluation.
    # Do any kind of evaluation here
    score.update(computeAllTFIDF(docs, termIds, docIds, index, search, weight))
    # score.update(COSINE_EVALUATION_FUNCTION)
    return score

# O(n^2)
def handleSearchQuery(query, termIds, docIds, index):
    # Searches for the query in the index

    # tdidf is a dictionary which has
    # a mapping structure as follows
    # <docId, tfidf>
    tfidfScores = {}

    # A list of documents which contain any of the words
    # in the query
    validDocs = set()

    # A list of documents which contain all of the words
    # in the query
    goodDocs = set()

    rawSearch = query.split()
    search = set()
    for word in rawSearch:
        if word in termIds:
            search.add(word)

    # First run a boolean search over the words in the query
    for word in search:
        checkDocs = booleanSearch(word, termIds, index)
        for doc in checkDocs:
            if doc not in validDocs:
                # Stops duplicate docIds from being added to the valid docs
                # list
                validDocs.add(doc)

    # Find all docs which have all words in the query, they are worth more.
    for doc in validDocs:
        containsAll = True
        for word in search:
            termId = termIds[word]
            validPages = index[termId]
            if doc not in validPages:
                containsAll = False
                break

        if containsAll:
            # Add it to the good docs
            goodDocs.add(doc)

    # Remove all the good docs from the valid docs
    for doc in goodDocs:
        validDocs.remove(doc)

    # print("Valid Docs: ", validDocs)
    # print("Good Docs: ", goodDocs)

    # Now compute tfidf of the document
    tfidfScores.update(computeScore(goodDocs, termIds, docIds, index, search, 2.0))
    tfidfScores.update(computeScore(validDocs, termIds, docIds, index, search, 1.0))
    return tfidfScores

# O(n^2)
def printTFIDF(tfidfScores):
        genexp = ((k, tfidfScores[k]) for k in sorted(tfidfScores, key=tfidfScores.get, reverse=True)[:5])
        for k, v in genexp:
            print("\n\tdocId = ", k, "\n\ttf-idf = ", v)

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
    # print('Building docTexts...')
    # docTexts = parseDocs()
    # if DEBUG or False:
    #     for docId in docTexts:
    #         print(docId, docTexts[docId])

    query = _input("Enter query: ").strip().lower()
    while query != "":
        tfidfScores = handleSearchQuery(query, termIds, docIds, index)
        printTFIDF(tfidfScores)
        query = _input("Enter query: ").strip().lower()

if __name__ == "__main__":
    main()
