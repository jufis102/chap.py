'''To do: 
	-wahrscheinlichsten vorgaenger und nachfolger auf ein keyword suchen
	 und ausgeben lassen
	-verfahren ueberlegen wenn mehrere gleiche ergebnisse
'''
import sqlite3
import re

def get_top_entropies(input):
	
	user_input = input.split(" ")
	#print user_input
	
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	top_entropie_words = []
	for element in user_input:
		#print element
		for row in c.execute('SELECT wort,entropy FROM Entropy WHERE wort = "'+element+'"'):
			ausgabe = row
			#print type(ausgabe)
		ausgabe = list(ausgabe)
		top_entropie_words.append(ausgabe)
		'''sortiert die Liste nach ihrer Entropy'''
		top_entropie_words.sort(key = lambda row: row[1])

	print top_entropie_words
	
	
	
	'''
	-top drei keywords sollen beachtet werden
	-es sollen die keywords mit der besten entropie(niedrigster wert) genommen werden
	-dann soll ein satz der das beste keyword enthaelt ausgegeben werden
	'''
	
	conn.commit()
	conn.close()

'''Keywordsuche zum ausgeben des wahrscheinlichsten Satzes'''
def search_for_keyword(input):
	
	response_predecessor = []
	response_successor = []

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

	for row in c.execute('SELECT kette, probability FROM Kette WHERE '
	'(kette like "%'+input+'%") ORDER BY probability DESC limit 1'):
		ergebnis = row

	ergebnis = list(ergebnis)
	satz = ergebnis[0]
	print satz

	conn.commit()
	conn.close()

	response_predecessor.append(satz)
	response_successor.append(satz)

# schleife solange bis abbruchsymbol

	def search_predecessor_chain(satz):

		conn = sqlite3.connect("chappies_brain.db")
		c = conn.cursor()

		satzsplit = satz.split(" ")
		neuerSatz = []
		for word in range(len(satzsplit)-1):
			try:
				#print satzsplit[word]
				neuerSatz.append(satzsplit[word])
			except: 
				pass
		neuerSatz = ' '.join(neuerSatz)
		print neuerSatz

		#try:
		for row in c.execute('SELECT kette, probability FROM Kette WHERE '
		'(kette like "%'+neuerSatz+'%") AND NOT (kette like "%'+satz+'%") ORDER BY probability DESC limit 1 '):
			ergebnis = row
		conn.commit()
		conn.close()
		
		ergebnis = list(ergebnis)
		ergebnis = ergebnis[0]


		vorgaenger_wort = ergebnis.split(" ")
		print ergebnis

		
		response_predecessor.insert(0,vorgaenger_wort[0])
	
		if "." in vorgaenger_wort[-1]:
			print "Vorheriger Satz erkannt! Beginne hier:"
		else:
			search_predecessor_chain(ergebnis)


	def search_successor_chain(satz):

		conn = sqlite3.connect("chappies_brain.db")
		c = conn.cursor()

		satzsplit = satz.split(" ")
		neuerSatz = []
		for word in range(len(satzsplit)):
			try:
				#print satzsplit[word+1]
				neuerSatz.append(satzsplit[word+1])
			except: 
				pass
		neuerSatz = ' '.join(neuerSatz)
		print neuerSatz
		''' to do: vernueftige fehlerbehandlung! wenn kein ergebnis mehr vorliegt was dannmachen?'''
		try:
			for row in c.execute('SELECT kette, probability FROM Kette WHERE '
			'(kette like "%'+neuerSatz+'%") AND NOT (kette like "%'+satz+'%") ORDER BY probability DESC limit 1 '):
				ergebnis = row
			
			ergebnis = list(ergebnis)
			ergebnis = ergebnis[0]
			conn.commit()
			conn.close()
		except:
			pass
		nachfolger_wort = ergebnis.split(" ")
		print ergebnis

		regex = "."
		
		try:
			response_successor.append(nachfolger_wort[-1])
		except: 
			pass
			
		print "nachfolger_wort[-1]" +nachfolger_wort[-1]
		
		if "." in nachfolger_wort[-1]:
			print "Found END of Sentence"
		else:
			search_successor_chain(ergebnis)


	search_predecessor_chain(satz)
	search_successor_chain(satz)
	
	print "predecessor: ",response_predecessor
	response_predecessor_finish = []
	for item in response_predecessor:
		if "." in item:
			index_dot = response_predecessor.index(item)
	print index_dot
	
	for item in range(index_dot,len(response_predecessor)):
		response_predecessor_finish.append(response_predecessor[item])
		
	response_predecessor = response_predecessor[-1]
	response_successor = response_successor[1:]
	

	#response_predecessor = ' '.join(response_predecessor)
	response_successor = ' '.join(response_successor)
	print response_predecessor_finish
	
	
	response_predecessor = ' '.join(str(element) for element in response_predecessor_finish)
	response_predecessor = response_predecessor.split('.',1)[1]
	
	response = response_predecessor+" "+response_successor
	print "predecessor: ",response_predecessor
	print "sucessor: ",response_successor

	return response

if __name__ == "__main__":
	get_top_entropies("this is that forfriends")
	#search_for_keyword("")

