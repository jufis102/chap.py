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
	
	#for row in c.execute('SELECT corpus FROM corpus'):
	#	sammler.append(row)
	#	print row
		
	#for item in sammler:
	#	marcov_chain.append(item[0])
	#print marcov_chain
	
	#length = len(marcov_chain)
	values = []
	
	for row in c.execute('SELECT  count(*) FROM corpus'):
		laenge = row[0]
	
	for row in c.execute('SELECT  corpus, count(*) as c, count(*) FROM corpus group by corpus'):
		probability = float(row[1])/float(laenge)
		#print row[0],probability
		values.append((row[0],probability))
	
	'''zaehlt die gleichen ketten und errechnet die wahrscheinlichkeiten 
	for chain in marcov_chain:
		zaehler = marcov_chain.count(chain)
		print chain , zaehler
	 
		probability = float(zaehler)/float(length)
		values.append((chain,probability))
		#gerundet = round(probability, 5)
		#print chain ,probability
		#print chain, gerundet
		
		einfuegen der wahrscheinlichkeiten in DB'''
	
	
	c.executemany("INSERT OR IGNORE INTO kette VALUES (?,?) ",values)

	conn.commit()
	conn.close()

#if __name__ == "__main__":
	#calculate_probability()
