import math
import sqlite3
import re
from collections import Counter
from cStringIO import StringIO

def delete_entropy():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	c.execute("DELETE from Entropy")
	conn.commit()
	conn.close()


def create_entropy():

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

	file_str = StringIO()

	for row in c.execute('SELECT corpus FROM corpus'):
		file_str.write(row[0])
	#print file_str
	
	StringList = (file_str.getvalue()).split(" ")
	
	countingWords = Counter(StringList)
	#print countingWords
	
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
	delete_entropy()
	create_entropy()
