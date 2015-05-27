import os
import sys
import collections
import json

#path for dumped crawl data
crawlDataPath = '/users/peternguyen/downloads/FileDump/';

#generated ids for terms and documents
termIdCount = 0
docIdCount = 0

#dictionary of term Ids
termIds = {}
#dictionary of document Ids
docIds = {}
#inverted index of term ids with corresponding list of document list
termIdDocList = {}

def isNumber(term):
    return term.isdigit()

#parse the file, build term id list, doc id list, inverted index
def parseFiles():
    global termIdCount
    global docIdCount
    global termIds
    global docIds
    global termIdDocList
    filesParsed = 0
    filesInDir = len(os.listdir(crawlDataPath))
    for fn in os.listdir(crawlDataPath):
        try:
            with open(crawlDataPath + fn) as data_file:
                data = json.load(data_file)
                #write docIds
                docId = data["id"]
                docUrl = data["_id"]
                docIds[docId] = docUrl
                #write termIds
                pageTerms = data["text"].split()
                for term in pageTerms:
                    termEncoded = term.encode('utf8').lower()
                    if(not isNumber(termEncoded)):
                        #add to list
                        value = termIds.get(termEncoded)
                        if(not value):
                            termIds[termEncoded] = termIdCount
                            # intialize inverted index
                            termIdDocList[termIdCount] = [docId]
                            #generate new term id
                            termIdCount = termIdCount + 1
                        else:
                            #build onto existing inverted index
                            docList = termIdDocList[value]
                            docList.append(docId)
                            termIdDocList[value] = docList
            #print progress of files processed
            filesParsed = filesParsed + 1;
            progress = (filesParsed / float(filesInDir)) * 100
            sys.stdout.write("Parsing files... %d%%   \r" % (progress) )
            if(progress != 100):
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')

        except ValueError:
            print('No valid json in file ' + fn)

def writeTermIdsToFile():
    global termIds
    #sort terms before writing
    termIds = collections.OrderedDict(sorted(termIds.items(), key=lambda x: x[1]))

    with open('termIds.txt', 'w') as f:
        termsWritten = 0
        totalTerms = len(termIds)

        f.write('Total Terms: ' + str(totalTerms) + "\n")
        for k, v in termIds.iteritems():
            #v is term Id, k is term
            f.write(str(v) + ' ' + k + '\n')
            termsWritten = termsWritten + 1
            #write progress to console
            progress = (termsWritten / float(totalTerms)) * 100
            sys.stdout.write("Writing termIds to file ... %d%%   \r" % (progress) )
            if(progress != 100):
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')

    print('Total terms: ' + str(totalTerms))

#write doc to files
def writeDocIdsToFile():
    global docIds
    with open('docIds.txt', 'w') as f:
        docIdsWritten = 0
        totalDocs = len(docIds)
        f.write('Total Docs: ' + str(totalDocs) + '\n')

        for k, v in docIds.iteritems():
            #k is docId, v is doc URL
            f.write(str(k) + ' ' + v  + '\n')
            #display progress in console
            progress = (docIdsWritten / float(totalDocs)) * 100
            sys.stdout.write("Writing termIds to file ... %d%%   \r" % (progress) )
            if(progress != 100):
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')

    print('Total Docs: ' + str(totalDocs))

def writeTermIdDocListToFile():
    global termIdDocList
    with open('invertedIndex.txt', 'w') as f:
        termsWritten = 0
        totalTerms = len(termIdDocList)

        for k, v in termIdDocList.iteritems():
            #k is termId, v is list of docIds
            docListString = str(len(v))
            for docId in v:
                docListString += ' ' + str(docId)
            f.write(str(k) + ' ' + docListString + '\n')
            termsWritten = termsWritten + 1;
            progress = (termsWritten / float(totalTerms)) * 100
            sys.stdout.write("Writing inverted index to file ... %d%%   \r" % (progress) )
            if(progress != 100):
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
    print('COMPLETED')

if __name__ == '__main__':
    print('Beginning file parsing')
    parseFiles()
    writeTermIdsToFile()
    writeDocIdsToFile()
    writeTermIdDocListToFile()
