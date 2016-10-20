'''To do:
	-ggf. wahrscheinlichkeiten runden?
'''
import sqlite3

def calculate_probability():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	sammler = []
	marcov_chain = []
	
	for row in c.execute('SELECT corpus FROM corpus'):
		sammler.append(row)
		#print row
		
	for item in sammler:
		marcov_chain.append(item[0])
	#print marcov_chain
	
	length = len(marcov_chain)
	
	'''zaehlt die gleichen ketten und errechnet die wahrscheinlichkeiten''' 
	for chain in marcov_chain:
		zaehler = marcov_chain.count(chain)
		#print chain , zaehler
	 
		probability = float(zaehler)/float(length)
		#gerundet = round(probability, 5)
		#print chain ,probability
		#print chain, gerundet
		
		'''einfuegen der wahrscheinlichkeiten in DB'''
		try:
			c.execute("INSERT INTO kette VALUES (?,?)",[chain,probability])
		except:
			pass
	conn.commit()
	conn.close()

if __name__ == "__main__":
	calculate_probability()
