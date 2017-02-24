'''To do:
	--anfangs und endsymbole in den ketten festlegen, damit saetze Sinn ergeben
'''
import sqlite3
from nltk import ngrams

n = 5

###############################
'''einlesen der Textdateien'''
def read_txt(filename):
	with open(filename) as data:
		content = data.read()
		return content
		
###############################
'''markov ketten erstellen '''
def create_marcov_chain(input):
	marcov_chain = []
	
	input = input.lower()
	input = input.rstrip()
	print(input)
	
	fivegrams = ngrams(input.split(), n)
	for grams in fivegrams:
		marcov_chain.append(list(grams))
	return marcov_chain

################################
def write_to_corpus(marcov_chain):
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
    
	for chain in marcov_chain:
		c.execute("INSERT INTO corpus VALUES (?,?)",[None, chain[0]+" "+chain[1]+" "+chain[2]+" "+chain[3]+" "+chain[4]])

	conn.commit()
	conn.close()

#################################
def read_corpus():
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

	for row in c.execute('SELECT * FROM corpus'):
		print(row)

	conn.commit()
	conn.close()

if __name__ == "__main__":
	text = read_txt("wine.txt")
	marcov_chain = create_marcov_chain(text)
	write_to_corpus(marcov_chain)
	#read_corpus()
