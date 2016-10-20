import math
import sqlite3
import re
from collections import Counter
#from nltk import SnowballStemmer

def create_entropy():

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	wordlist = []
	stringList = []
	string = ""
	
	for row in c.execute('SELECT corpus FROM corpus'):
		wordlist.append(row)
	#print wordlist
	
	'''typeUmwandlung von Tuple in String zur weiterverarbeitung des Corpus'''
	for item in wordlist:
		#print item[0]
		item = " "+item[0]
		string += item
	StringList = string.split(" ")
	
	countingWords = Counter(StringList)
	#print countingWords
	'''Woerter stemmen, also auf ihren Wortstamm zurueckfueren'''
	
	#stemmer1 = SnowballStemmer('german')

	#stem =stemmer1.stem(wordlist)
	#print stem
	
	'''gesamte Laenge des Corpus '''
	laenge = len(countingWords)
	#print "Corpuslaenge: ",laenge
	
	'''berechnung der Wortwahrscheinlichkeiten und der Entropy'''
	for key,value in countingWords.iteritems():
		#print key,value
		wahrscheinlichkeit = float(value)/float(laenge)
		#print "Wort: ", key, "| Worthaeufigkeit: ",value, "| Wahrscheinlichkeit: ", wahrscheinlichkeit
	
		entropy = wahrscheinlichkeit*math.log(wahrscheinlichkeit)*-1
		#print "Entropy = ", entropy
		
		'''einfuegen in die DB'''
		try:
			c.execute("INSERT INTO entropy VALUES (?,?)",[key,entropy])
		except:
			pass

	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	create_entropy()
