'''To do:
	-ggf. wahrscheinlichkeiten runden?
'''
import sqlite3

def drop_probability():
	
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	c.execute("DELETE from Kette")
	conn.commit()
	conn.close()

def calculate_probability():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	sammler = []
	marcov_chain = []
	
	values = []
	
	''' hole zahl aller elemente in db'''
	for row in c.execute('SELECT  count(*) FROM corpus'):
		laenge = row[0]
		
	'''count vorkommen einer kette'''
	for row in c.execute('SELECT  corpus, count(*) as c, count(*) FROM corpus group by corpus'):
		probability = float(row[1])/float(laenge)
		#print row[0],probability
		values.append((row[0],probability))
		
		
	'''einfuegen der wahrscheinlichkeiten in DB'''
	'''executemany schreibt die ganze liste auf einmal. keine iteration noetig'''
	c.executemany("INSERT OR IGNORE INTO kette VALUES (?,?) ",values)

	conn.commit()
	conn.close()

if __name__ == "__main__":
	calculate_probability()
