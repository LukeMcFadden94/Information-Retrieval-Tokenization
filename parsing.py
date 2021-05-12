import re
import os
import zipfile
from nltk.stem import PorterStemmer

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
token_regex = re.compile('(?:\w+)(?:\,?\.?\w+)*')

def parseFunc(term = "", docID = ""):
    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()
    
    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

    # Create list of stopwords
    stopwords = []
    with open("stopwords.txt", "r") as f:
        for word in f:
            word = word.replace("\n", "")
            stopwords.append(word)
    stopwords.append("_")

    all_tupleList = {} # stores tupleList for all documents
    all_tupleList_counter = 0

    all_doc_word_count = {} # stores word count for each document
    #all_doc_word_count_counter = 0

    all_word_dict = {} # stores all unique words across all documents
    all_word_dict_counter = 1

    all_docID_index_Val = 0
    all_docID_counter = 0

    doc_dict = {}
    position_list = []

    # if(term != ""):     # user passed in a term
    #     userTerm = term

    canbreak = 0
    fileNum = 1
    for file in allfiles: # per file
        # if(canbreak == 1): # if user document was found in prior file, can break loop
        #     break

        #print("In file #:", fileNum)
        fileNum += 1

        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

            docNum = 1
            for docpos, document in enumerate(result): # per document
                # if(canbreak == 1):  # if user document was found prior, can break loop
                #     break

                #print("In doc #:", docNum)
                docNum += 1
                
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                #if(docno == docID):
                    #canbreak = 1
                #if(docID != "" and docID != docno):
                    #continue

                # Retrieve contents of TEXT tag
                text = "".join(re.findall(text_regex, document))\
                        .replace("<TEXT>", "").replace("</TEXT>", "")\
                        .replace("\n", " ")
                
                # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 

                # lowercase all words
                text = text.lower()

                # remove punctuation and create tokens
                res = token_regex.findall(text)
                
                # remove stop words
                gowords = []
                baddies = []
                for word in res:
                    if word not in stopwords:
                        gowords.append(word)
                    else:
                        baddies.append(word)

                # print(gowords)
                # print("\n\n\n")
                # print(baddies)

                stemmer = PorterStemmer()

                # step 3 Remove stemmed words
                stemresults = []
                for word in gowords:
                    stemword = stemmer.stem(word)
                    stemresults.append(stemword)

                # step 3 - build index
                # tuple includes: (TermIds, DocIds, termInfoKey)
                # TermIds: {word:uniqueId}
                # DocIds: {documentId:documentName}
                # termInfoKey: {uniqueId:(number of occurences, frequency/tf )}             

                tupleList = [] # stores entries with 3 aspects: termId, docId, position
                word_dict = {} # store unique term keys
                unique_word_count = 0
                doc_word_count = 0
                word_count_dict = {}
                word_count_in_doc = 0
                doc_unique_word = {}
                all_docID_counter += 1

                for word in stemresults:
                    doc_word_count += 1                      

                    # all_word_dict:
                    # each index holds -
                    # 1 key (word), 4 values
                    # {word, [0 all_word_dict_counter, 1 docs_containing_term, 2 all_freq, 3 term's freq in a specific doc]}

                    if word not in word_dict:
                        unique_word_count += 1
                        word_dict[word] = unique_word_count
                        uniqueId = unique_word_count
                        word_count_dict[word] = 1
                    else:
                        uniqueId = word_dict[word]
                        word_count_dict[word] += 1

                    # check word uniqueness across all documents
                    if word in all_word_dict:           # repeat occurence of word
                        if word not in doc_unique_word:
                            doc_unique_word[word] = True
                            all_word_dict[word][1] += 1 # increase # of docs with term
                        all_word_dict[word][2] += 1     # increase overall term count
                    else:   # first occurence of word ever
                        doc_unique_word[word] = True        
                        all_word_dict[word] = [all_word_dict_counter, 1, 1, 0]
                        all_word_dict_counter += 1

                    if((word == term) and (docID == docno)): # if current word matches user term, then add the position to list and increase freq counter
                        position_list.append(doc_word_count) 
                        word_count_in_doc += 1



                    # store info in tuple list
                    tupleList.append((word_dict[word], docpos, doc_word_count))

                doc_dict[docno] = all_docID_counter
                all_doc_word_count[all_docID_index_Val] = doc_word_count
                all_tupleList[all_tupleList_counter] = tupleList
                all_docID_index_Val += 1

                if((docID == docno) and (term in all_word_dict)): # if current docno matches user's docID and the user's term is 
                    all_word_dict[term][3] = word_count_in_doc    # in the all_word_dict, add the total freq to the specific term's index
                
                #if(docID == docno):
                    #print(stemresults)
                ### end specific document loop      
                

    return all_tupleList, all_doc_word_count, doc_dict, all_word_dict, position_list

    ### end looping of allfiles

                
