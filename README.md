Made by Luke McFadden

Note, this saves to memory and not to disk, so every run of this program will take about 1-2 minutes to fully parse through the entire collection of files!

A combination of dictionaries and lists are used to keep track of and store important aspects that the assignment asks for.
After documents are extracted, the words within stopword.txt are extracted and used for a stopwords list. Any words found within this list are removed from allthe documents.
Stemming is performed after stop word removal.
Dictionaries and lists are used and updated as each document is iterated through. Aspects like document word count, a term's overall frequency, term positions in a document, etc, are stored.

The nltk.stem library is used, specifically the PorterStemmer() function. 
After stop words are removed, the remaining words are passed through this function to perform stemming.

How to run code:
The program accepts 3 different forms of input. DOCNAME or TERM are included for as reference. Said forms are shown below:

.\read_index.py --doc AP890123-0321

.\read_index.py --term evasion

.\read_index.py --term evasion --doc AP890123-0321


--doc and --term can be used on their own. If --term and --doc are used together, --term must be used before --doc.

There are no checks to ensure the spelling of TERM or DOCNAME arguments.

The DOCNAME argument needs to be spelled with a capital 'AP'.

The code can handle if capitalization or punctuation occurs in the TERM argument.
For example, a TERM such as UNITED, would become united.

Any TERMs which include an apostrophe in them, should have the entire TERM enclosed within " ".
For example, the TERM Reagan's should be expressed as "Reagan's". 
Would look like:
--term "Reagan's"
The term will become reagan.

