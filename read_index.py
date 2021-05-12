# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import sys
import re
from nltk.stem import PorterStemmer
from parsing import *

token_regex = re.compile('(?:\w+)(?:\,?\.?\w+)*')

all_tupleList = {}
all_doc_word_count = {}
doc_dict = {}
all_word_dict = {}
position_list = []
stemmer = PorterStemmer()

# def getArguments(list:arg):
#     docID = ""
#     term = ""
#     arglen = len(arg)

#     has_doc = "--doc" in arg && arglen >=3
#     has_term = "--term" in arg && arglen >=3
#     has_both = has_doc && has_term && arglen >=5

#     if has_doc:
#         doc_index = arg.index("--doc") + 1
#         docID = arg[doc_index]
#     if has_term:
#         term_index = arg.index("--term") + 1
#         term = arg[term_index]

#     return docID, term

def docFunct(docID):
    all_tupleList, all_doc_word_count, doc_dict, all_word_dict, position_list= parseFunc("", docID)
    if docID in doc_dict:
            print("Listing for the document:", docID)
            print("DOCID:", doc_dict[docID])

    for doc_count in all_doc_word_count:
        if(doc_count == doc_dict[docID]):
            print("Total terms:", all_doc_word_count[doc_count])  
    
    return

def termFunct(term):
    # get stem word
    stemterm = stemmer.stem(term).lower()
    regterm = re.match(token_regex, stemterm)
    regterm = regterm.group(0)
    all_tupleList, all_doc_word_count, doc_dict, all_word_dict, position_list= parseFunc(regterm, "")    
    # 1 key (word), 3 values
    # {word, [0 all_word_dict_counter, 1 docs_containing_term, 2 all_freq]}
    if regterm in all_word_dict:
        val = all_word_dict[regterm]
        print("Listing for term:", term)
        print("TERMID:", val[0])
        print("Number of documents containing term:", val[1])   
        print("Term frequency in corpus:", val[2])

def bothFunct(term, docID):
    # get stem word
    stemterm = stemmer.stem(term).lower()
    regterm = re.match(token_regex, stemterm)
    regterm = regterm.group(0)
    all_tupleList, all_doc_word_count, doc_dict, all_word_dict, position_list= parseFunc(regterm, docID)
    if regterm in all_word_dict:
        val = all_word_dict[regterm]
        print("Inverted list for term:", term)
        print("In document:", docID)
        print("TERMID:", val[0])
        print("DOCID:", doc_dict[docID])
        print("Term frequency in document:", all_word_dict[regterm][3])
        print("Positions:", position_list)


args = sys.argv
length = len(sys.argv)
length -= 1

if(length == 2):
    flag = args[1]
    obj = args[2]

    if(flag == "--doc"): 
        docFunct(obj) 
    elif(flag == "--term"):
        termFunct(obj)
    else:
        print("Error - invalid flag and/or docname/term\n")

elif(length == 4):
    flag = args[1]
    obj = args[2]
    flag2 = args[3]
    obj2 = args[4]

    if (flag != "--term"):
        print("Error - expected --term as first argument\n")
    elif (flag2 != "--doc"):
        print("Error - expected --doc as third argument\n")
    else:
        bothFunct(obj, obj2)

else:
    print("Error - invalid input\n")


