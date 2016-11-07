'''To do:
	--anfangs und endsymbole in den ketten festlegen, damit saetze Sinn ergeben
'''
import sqlite3

###############################
'''einlesen der Textdateien'''
def read_txt(filename):
	with open(filename) as f:
		content = f.read().decode('utf-8')
		return content
		
###############################
'''markov ketten erstellen '''
def create_marcov_chain(input):
	marcov_chain = []
	
	#input.lower macht alle woerter klein
	split = (input.lower()).split(" ")
	
	print "Split: ",split
	try:
		for i in range(len(split)):
			print i
			marcov_chain.append([split[i],split[i+1],split[i+2],split[i+3],split[i+4]])
			print split[i], split[i+1],split[i+2],split[i+3],  "->", split[i+4]
	except:
		pass
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
		print row

	conn.commit()
	conn.close()

if __name__ == "__main__":
	#content = read_txt("Outside of physics we know nothing of action at a distance.")
	#print type(content)
	marcov_chain = create_marcov_chain("Outside of physics we know nothing of action at a distance of blabla.")
	write_to_corpus(marcov_chain)
	#read_corpus()
