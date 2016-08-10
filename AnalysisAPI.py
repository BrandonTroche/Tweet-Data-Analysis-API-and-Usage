import sys
import csv
import tweepy
from math import log
from math import sqrt
from math import acos
from math import degrees

__author__ = "Brandon Troche"
__copyright__ = "Copyright 2016, Profil-d"
__credits__ = ["Brandon Troche", "William Wu", 
               "Ada Chen", "Fabio Francios", "Felix Grezes"]
__maintainer__ = "Brandon Troche"
__documentor__ = "Brandon Troche"
__email__ = "bttroche@gmail.com"
__git__ = "www.github.com/BrandonTroche"
__special_thanks__ = "Fabio Francios"

reload(sys)
sys.setdefaultencoding('utf-8')


"""
-	Show buzz words/topics that you share with a candidate
-   single tweet analysis for most similar tweet from candidate
-	Only have the candidate tweets take 100 instead of 1000.
"""

"""
parseCSV_Dictionary(nameOfCSV)

parameters:
	- nameOfCSV: The name of a csv file that contains a users tweets. 

returns: 
	- A dictionary created to hold all terms used in the csv file (document) as keys
	and their number of occurance in the document as values. 

"""
def parseCSV_Dictionary(nameOfCSV):
	csvfile = open(nameOfCSV, 'r')
	reader = csv.DictReader(csvfile, fieldnames = ("name", "time", "tweets"))

	Tweet = ""
	wordsDictionary = {}

	for row in reader:
		TweetTweet = str("").join(str(row['tweets']))

		Tweet = TweetTweet
		tweetArray = Tweet.split()
		tweetSize = len(tweetArray)


		WordAnalysis(wordsDictionary, tweetSize, tweetArray)

	csvfile.close()

	return wordsDictionary

"""
parseCSV_Vector(nameOfCSV)

parameters:
	- nameOfCSV: The name of a csv file that contains a users tweets. 

returns: 
	- An array or vector that contains all the users tweets that exist in
	a csv file (document) and sorted in the order in which they are appended 
	is in occordance with their time of occurance. 

"""
def parseCSV_Vector(nameOfCSV):
	csvfile = open(nameOfCSV, 'r')
	reader = csv.DictReader(csvfile, fieldnames = ("name", "time", "tweets"))

	wordsArray = []

	for row in reader:
		TweetTweet = str("").join(str(row['tweets']))

		tweetArray = TweetTweet.split()

		for items in tweetArray:
			if items not in wordsArray:
				wordsArray.append(items.lower())

	csvfile.close()

	return wordsArray

"""
cosineSimilarity(dotProduct, vectorNormA, vectorNormB)

parameters:
	- dotProduct: The respective dot product of two vectors.
	- vectorNormA: The norm of the vector of the first document.
	- vectorNormB: The norm of the vector of the second document. 
	

returns:
	- The cosine similarity of both documents to each other. 

Give the formula:

	VectorA.VectorB / sqrt( norm(VectorA) * norm(VectorB) )

"""
def cosineSimilarity(dotProduct, vectorNormA, vectorNormB):
	Numerator = dotProduct
	Denominator = sqrt(vectorNormA * vectorNormB)

	return Numerator/Denominator
	#return degrees(acos(Numerator/Denominator))

"""
vectorNorm(Vector, SemanticDictionary)

parameters:
	- Vector: A vector or array that contains terms present in specific a document. 
	

returns:
	- The norm of the vector. [i.e. the sum of all elements in the vector squared.] 

"""
def vectorNorm(Vector, SemanticDictionary):
	total = 0
	for i in Vector:
		total += SemanticDictionary[i]**2

	return total

"""
def vectorDotProduct(VectorA, DictionaryA, DictionaryB)

parameters:
	- DictionaryA: A dictionary that contains all of the terms and their values in the first 
	document with respect to all terms present in both documents.
	- DictionaryB: A dictionary that contains all of the terms and their values in the second 
	document with respect to all terms present in both documents.
	- VectorA: An augmented vector or array containing the terms present in both documents 
	with respect to the first documents terms. [i.e. the terms present in the first document
	come first in the array and are then followed by the terms in the second document. These 
	terms are listed in order of appearance without repetition.]
	

returns:
	- The respective dot product of both arrays/vectors present in the variables 'VectorA' and
	'VectorB.'

How?
	- This function uses the dictionaries 'DictionaryA' and 'DictionaryB' to store the values of
	all terms in the two documents. "Document A" would be the first document and "Document B" would
	be the second where the dictionaries with the respective tag letters hold that documents values. 
	The dot product is computed by using the universal vector 'VectorA' that contains all terms in 
	order of appearance without repetition assuming 'Document A' is read first. The terms in this 
	vector are checked with the dictionaries holding the values to compute accurately positioned
	vector elements.

For Example:

	VectorA = ["jack", "loves", "me", "more", "than", "mark", "jason", "likes"]
	DictA = {"jack":1, "loves":2, "me":2, "more":1, "than":1, "mark":1, "jason":0, "likes":0}
	DictB = {"jack":1, "loves":1, "me":2, "more":1, "than":1, "mark":0, "jason":1, "likes":1}

	print AnalysisAPI.vectorDotProduct(VectorA, DictA, DictB)

	THE ABOVE CODE SHOULD OUTPUT: 9.

	SENTENCE 1: JACK LOVES ME MORE THAN MARK LOVES ME
	SENTENCE 2: JACK LOVES ME MORE THAN JASON LIKES ME

***** This has a more in-depth explaination than the other funtions because I figured
some people who read this documentation might not understand what I had in mind for this 
implementation or may have some questions about how it works and links together with 
itself in general. *****

"""
def vectorDotProduct(VectorA, DictionaryA, DictionaryB):
	total = 0
	for i in VectorA:
		total += DictionaryA[i] * DictionaryB[i]

	return total

"""
createUserDictionary(DictionaryA, VectorA, VectorB)

parameters:
	- DictionaryA: A dictionary that contains all of the terms in the first document.
	- VectorA: A vector or array containing the terms present in the first document.
	- VectorB: A vector or array containing the terms present in the second document. 

returns:
	- A dictionary that will contain all of the words present in both documents. This
	dictionary is only to be used as a reference to the first document when calculating
	cosine similarity as it contains 0's in all the places where words appear in the second
	document that do not occur in the first appended to the end of the vector. 

Augments:
	- This function also changes the contents of the array passed in variable 'VectorA' to also
	contain all of the words present in the array 'VectorB' that are not present in 'VectorA.' 
	This means all of the words present in the document are now stored in 'VectorA' based on the
	contents of the first document. This allows for an accurate calculation of vector dot product
	later on.

"""
def createUserDictionary(DictionaryA, VectorA, VectorB):
	for term in VectorB:
		if(not DictionaryA.has_key(term)):
			VectorA.append(term)
			DictionaryA[term] = 0

	newDictionary = {}

	for keys in DictionaryA:
		newDictionary[keys] = 0

	return newDictionary


"""
createArray(SemanticDictionary)

parameters:
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 

returns:
	- An array created based on the contents of the dictionary passed in 'SemanticDictionary'.
	This array is created, sorted from least to greatest occurance in the document according to
	its value in the dictionary and then filtered for stop words. 

"""
def createArray(SemanticDictionary):
	wordsArray = []

	for keys in SemanticDictionary:
		wordsArray.append(keys)

	copyDict = SemanticDictionary.copy()

	wordsArray = sortArray(wordsArray, copyDict)

	stopWordsFilter(wordsArray)


	return wordsArray


"""
WordAnalysis(SemanticDictionary, Size, TweetArray)

parameters:
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 
	- Size: The size of the array given as a parameter in 'TweetArray'.
	- TweetArray: An array or vector populated with terms in the document.  

Augments:
	- Does not return an object. Instead this function augments the contents of 
	the dictionary passed in the parameter 'SemanticDictionary' in the following
	fashion: if the term already exists in the dictionary as a key then we increment
	the value of that key where the value represents the amount of times the key(term) 
	was used in the document. If the term does not exist in the dictionary then it has
	not been seen yet and we create a space in the dictionary for a new key and set its
	value to 1.

"""
def WordAnalysis(SemanticDictionary, Size, TweetArray):
	for i in range(Size):
		if(SemanticDictionary.has_key(TweetArray[i].lower())):
			SemanticDictionary[TweetArray[i].lower()] += 1
		else: 
			SemanticDictionary[TweetArray[i].lower()] = 1


"""
mostUsed(numberOfMostUsed, termArray, SemanticDictionary)

*** Use only on a sorted array ***
parameters:
	- numberOfMostUsed: Signifies the number of terms you'd like to print.
	- termArray: An array or vector populated with all the terms in the document without 
	repetition.
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 

prints:
	- A specified number of terms and their number of uses in the document from greatest to 
	least used.
"""
def mostUsed(numberOfMostUsed, termArray, SemanticDictionary):
	if numberOfMostUsed > len(termArray):
		numberOfMostUsed -= numberOfMostUsed - len(termArray)
	for terms in range(numberOfMostUsed):
		print "The term '%s' appeared '%s' times." % (termArray[len(termArray) - terms - 1], checkTerm(termArray[len(termArray) - terms - 1], SemanticDictionary))

"""
checkTerm(Term, SemanticDictionary)

parameters:
	- Term: Any string in all lower case.
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 

returns:
	- The corresponding value of a key in a dictionary. For this use, it will specifically
	return the number of times the term was used in the document. 
"""
def checkTerm(Term, SemanticDictionary):
	if(SemanticDictionary.has_key(Term)):
		return SemanticDictionary[Term]
	else:
		return 0

"""
highestTerm(SemanticDictionary)

parameters:
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 

returns:
	- The string in the document that appears the most amount of times. 

deletes:
	- deletes from the dictionary the string that was returned. 
"""
def highestTerm(SemanticDictionary):
	tempLargest = 0
	tempString = "All equally used"
	for i in SemanticDictionary:
		if SemanticDictionary[i] > tempLargest:
			tempLargest = SemanticDictionary[i]
			tempString = i
	del SemanticDictionary[tempString]
	return tempString


"""
sortArray(termArray, SemanticDictionary)

parameters:
	- termArray: An array or vector containing all the terms in the document. 
	- SemanticDictionary: A dictionary holding the terms in the document without repetition
	as keys and the number of times they appear in the document as values. 

returns:
	- A sorted array of terms based on the dictionary containing all terms and values in
	the document.

sort order: 
	- least to greatest use of the term in the document. Such that the first element of the
	array or vector is the word that occurs the least amount of times and the last element in 
	the array or vector is the word that occurs the most amount of times. 
"""
def sortArray(termArray, SemanticDictionary):
	sortedArray = []
	for objs in termArray:
		sortedArray.insert(0, highestTerm(SemanticDictionary))
	return sortedArray

"""
pullTweets(arr, name)

parameters:
	- arr: An empty array that can hold the tweets of a defined user. 
	- name: The twitter handle of a user whose tweets with be pulled.

Augments:
	- Does not return an object. Instead this function augments the contents of 
	the array in the parameter 'arr' to hold the tweets pulled from the users
	account based on their twitter handle stored in 'name'. 

"""
def pullTweets(arr, name):
	consumer_token = '9VvsBn2c4Q5wBSoA3MsBZLbFp'
	consumer_secret = 'bVPdCJWsjw6Q75UO6FqSPYLJottjbj0Q4kkO46PjyLhlbqp9Il'
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	api = tweepy.API(auth)

	for tweet in tweepy.Cursor(api.user_timeline, screen_name=name).items(100):
		arr.append(tweet)

"""
writeToFile(openfile,arr)

parameters:
	- openfile: a variable containing an open csv file that is opened with the intention to 
	write back. [i.e... open('csv', 'wb')]
	- arr: an array populated with the tweets of a user.

Augments:
	- Does not return an object. Instead this function augments the contents of 
	the csv file to contain all of the tweets of the user in order of occurance. 

"""
def writeToFile(openfile,arr):
    openfile.write("name,time,tweets\n")
    for tweet in arr:
        openfile.write(tweet.user.name + ',' + \
        str(tweet.created_at) + ',' + tweet.text.replace(',','',20).replace('\n',' ',20).replace('.','',20).replace('-',' ',20) +'\n')

"""
termDocWeight(termFrequencyInDoc, totalTermsInDoc, termFreqInCorpus, totalDocs)

parameters:
	- termFreqInDoc: The amount of times a term or string occurs in the document.
	- totalTermsInDoc: The total amount of different terms that exist in the document.
	- termFreqInCorpus: The amount of times a term occurs in the entire corpus.
	- totalDocs: The total amount of documents that make up the corpus.

returns:
	- The calculated term frequency inverse document frequency of that term in the corpus. 

"""
def termDocWeight(termFrequencyInDoc, totalTermsInDoc, termFreqInCorpus, totalDocs):
	tf = float(termFrequencyInDoc) / float(totalTermsInDoc) 
	docFreq = totalDocs / termFreqInCorpus 
	idf = log(docFreq)

	return tf*idf

"""
stopWordsFilter(termArray)

parameters:
	- termArray: An array or vector populated with the terms that exist in the document.

augments:
	- Does not return an object. Instead this function augments the contents of 
	the array given in 'termArray' to delete words that appear in a list of predetermined 
	stop words.  
"""
def stopWordsFilter(termArray):
	stopWordList = "a about above after again against all am an and any are \
	aren't as at be because been before being below between both but by can't \
	cannot could couldn't did didn't do does doesn't doing don't down during each \
	few for from further had hadn't has hasn't have haven't having he he'd he'll he's\
	 her here here's hers herself him himself his how how's i i'd i'll i'm i've if in \
	 into is isn't it it's its itself let's me more most mustn't my myself no nor not of \
	 off on once only or other ought our ours ourselves out over own same shan't she she'd \
	 she'll she's should shouldn't so some such than that that's the their theirs them \
	 themselves then there there's these they they'd they'll they're they've this those \
	 through to too under until up very was wasn't we we'd we'll we're we've were weren't \
	 what what's when when's where where's which while who who's whom why why's with won't \
	 would wouldn't you you'd you'll you're you've your yours yourself yourselves just can de la"

	stopWords = []
	stopWords = stopWordList.split()
	toRemove = []
	for term in termArray:
		for wordz in stopWords:
			if(term == wordz):
				toRemove.append(term)

	for objects in toRemove:
		termArray.remove(objects)

