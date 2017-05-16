'''To do:
	--anfangs und endsymbole in den ketten festlegen, damit saetze Sinn ergeben
	
	#sqlite3 chappies_brain.db < dump.sql 	
'''
import sqlite3
from nltk import ngrams
from create_entropy import create_entropy
from create_probabilities import calculate_probability, drop_probability

n = 4

###############################
'''einlesen der Textdateien'''
def read_txt(filename):
	with open(filename) as data:
		content = data.read()
		return content
		
def tokenize_sentences(input):
	clean_sentences = []
	from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
	punkt_param = PunktParameters()
	punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
	sentence_splitter = PunktSentenceTokenizer(punkt_param)
	input = input.rstrip()
	sentences = sentence_splitter.tokenize(input)
	# erkenne Sätze, Satz-Tokenizer
	for sentence in sentences:
		sentence = sentence[:-1] # Entferne den Punkt jeden Satzes
		if not (len(sentence)) < 20: # Wenn der Satz weniger als X Zeichen hat, beachte diesen nicht mehr
			sentence = sentence.replace("\n","") # entferne \n und ersetze mit nichts
			sentence = sentence.replace("/"," ") # entferne / und ersetze mit Leerzeichen
			clean_sentences.append("!$! "+sentence+" !€!") # Gebe Satz Start und Endsymbol und übergebe an Liste, clean_sentences
	#print(clean_sentences)		
	return clean_sentences
		
###############################
'''markov ketten erstellen '''
def create_marcov_chain(input):
	marcov_chain = []
	for i in input:
		i = i.lower()
		i = i.rstrip()
		#print(i)
		
		fivegrams = ngrams(i.split(), n)
		for grams in fivegrams:
			marcov_chain.append(list(grams))
	return marcov_chain

################################
def write_to_corpus(marcov_chain):
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
    
	for chain in marcov_chain:
		c.execute("INSERT INTO corpus VALUES (?,?)",[None, chain[0]+" "+chain[1]+" "+chain[2]+" "+chain[3]])#+" "+chain[4]])

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
	sentences = tokenize_sentences(text)

	marcov_chain = create_marcov_chain(sentences)
	for i in marcov_chain:
		print(i)

	

	
	write_to_corpus(marcov_chain)
	drop_probability()  # delete old probabilities
	calculate_probability() # calculate new probabilites
	create_entropy()
	#read_corpus()
