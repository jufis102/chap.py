import math
import sqlite3
import re
from collections import Counter
from io import StringIO
import time

def delete_entropy():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	c.execute("DELETE from Entropy")
	conn.commit()
	conn.close()


def create_entropy():

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

	file_str = []

	for row in c.execute('SELECT corpus FROM corpus'):
		kette = row[0].rstrip()
		kette = row[0].split(" ")  #ToDO: sonderzeichen entfernen damit einzelnes wort erkannt und berechnet wird
		for i in kette: 
			file_str.append(i)
			
	countingWords = Counter(file_str)
	from nltk import SimpleGoodTuringProbDist, FreqDist
	fd = FreqDist(countingWords)
	p = SimpleGoodTuringProbDist(fd)	
	
	#print countingWords
	'''gesamte Laenge des Corpus '''
	laenge = len(countingWords)
	#print "Corpuslaenge: ",laenge
	#print(countingWords)
	#print(round(p.prob('this'), 4))
	for i in fd:
		entropy = (round(p.prob(i), 7))
		try:
			c.execute("INSERT INTO entropy VALUES (?,?)",[i,entropy])
		except:
			pass
	'''berechnung der Wortwahrscheinlichkeiten und der Entropy'''
	
	'''
	time.sleep(5000)
	for key,value in countingWords.items():
		#print key,value
		wahrscheinlichkeit = float(value)/float(laenge)
		#print "Wort: ", key, "| Worthaeufigkeit: ",value, "| Wahrscheinlichkeit: ", wahrscheinlichkeit
	
		entropy = wahrscheinlichkeit*math.log(wahrscheinlichkeit)*-1
		print("Entropy = ", entropy)
		
		
		#try:
		#	c.execute("INSERT INTO entropy VALUES (?,?)",[key,entropy])
		#except:
		#	pass
	'''
	conn.commit()
	conn.close()
	
#if __name__ == "__main__":
#	delete_entropy()
#	create_entropy()
