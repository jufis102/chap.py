'''To do:
	-ggf. wahrscheinlichkeiten runden?
'''
import sqlite3
import time
from nltk import SimpleGoodTuringProbDist, FreqDist

def drop_probability():
	
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	c.execute("DELETE from Kette")
	conn.commit()
	conn.close()

def calculate_probability():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	kette_dict = {}
	sammler = []
	marcov_chain = []
	
	values = []
	
	''' hole zahl aller elemente in db'''
	for row in c.execute('SELECT  count(*) FROM corpus'):
		laenge = row[0]
		
	'''count vorkommen einer kette'''
	for row in c.execute('SELECT  corpus, count(*) FROM corpus group by corpus'):
		kette_dict[row[0]] = row[1]
		#probability = float(row[1])/float(laenge)
		#print(row[0],probability)
		#values.append((row[0],probability))
	conn.commit()
	conn.close()
	
	#print(kette_dict)
	fd = FreqDist(kette_dict)
	print(fd)
	p = SimpleGoodTuringProbDist(fd)
	print("Run Simple Good Turing",fd)
	#time.sleep(5000)
	for i in fd:
		#print(i)
		pk = p.prob(i)
		values.append((i,pk))
		
		#c.execute("INSERT INTO kette VALUES (?,?)",[i,pk])

	drop_probability()
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()	
	'''einfuegen der wahrscheinlichkeiten in DB'''
	'''executemany schreibt die ganze liste auf einmal. keine iteration noetig'''
	c.executemany("INSERT OR IGNORE INTO kette VALUES (?,?) ",values)

	conn.commit()
	conn.close()

if __name__ == "__main__":

	#drop_probability()
	calculate_probability()
	
