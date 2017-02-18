'''To do: 
	-verfahren ueberlegen wenn mehrere gleiche ergebnisse
	-ordentliche Stoppwortabfrage, anfangsymbole, endsymbole 
	woerter in woertern duerfen nicht beruecksichtigt werden
'''
import sqlite3
import re


def get_top_entropies(input):
	
	user_input = input.split(" ")
	#print "Input: ",user_input
	
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	top_entropie_words = []
	for element in user_input:
		#print "Element: " ,element
		# if sql null
		for ausgabe in c.execute('SELECT wort,entropy FROM Entropy \
		WHERE wort = "'+element+'" ORDER BY entropy DESC limit 1'):
			
			print "sql Entropy: ",ausgabe
			
		cursor = c.execute('SELECT wort,entropy FROM Entropy \
		WHERE wort = "'+element+'" ORDER BY entropy DESC limit 1')
		cursor_len = len(cursor.fetchall())
		print "Cursor_len: ", cursor_len
		
		if cursor_len > 0:
			ausgabe = list(ausgabe)
			#print ausgabe
			top_entropie_words.append(ausgabe)
		
		'''sortiert die Liste nach ihrer Entropy'''
	top_entropie_words.sort(key = lambda row: row[1])

	print "Top_Entropy_Words: ",top_entropie_words

	top_3_words = top_entropie_words[0:3]
	top_3_words = [item[0] for item in top_3_words]
	print "Top 3: ",top_3_words
	'''
	-top drei keywords sollen beachtet werden
	-es sollen die keywords mit der besten entropie(niedrigster wert) genommen werden
	-dann soll ein satz der das beste keyword enthaelt ausgegeben werden
	'''
	conn.commit()
	conn.close()
	
	return top_3_words
	
'''Keywordsuche zum ausgeben des wahrscheinlichsten Satzes'''
def search_for_keyword(top_3_words):

	response_predecessor = []
	response_successor = []

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

	#top1 = top_3_words[0]
	#top2 = top_3_words[1]
	#top3 = top_3_words[2]
	try:
		top1 = top_3_words[0]
	except:
		top1 = "null"
	try:
		top2 = top_3_words[1]
	except:
		top2 = "null"
	try:
		top3 = top_3_words[2]
	except:
		top3 = "null"
	
	print "Top1= ",top1," Top2= ",top2," Top3= ",top3

	for row in c.execute('SELECT kette, probability FROM Kette \
	WHERE \
	   (kette like ? AND kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	ORDER BY probability DESC limit 1',["%"+" "+top1+" "+"%","%"+" "+top2+" "+"%","%"+" "+top3+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top2+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top3+" "+"%","%"+" "+top2+" "+"%","%"+" "+top3+" "+"%","%"+" "+top1+" "+"%",\
	"%"+" "+top2+" "+"%","%"+" "+top3+" "+"%"]):
		ergebnis = row

	TopWords = c.execute('SELECT kette, probability FROM Kette \
	WHERE \
	   (kette like ? AND kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	ORDER BY probability DESC limit 1',["%"+" "+top1+" "+"%","%"+" "+top2+" "+"%","%"+" "+top3+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top2+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top3+" "+"%","%"+" "+top2+" "+"%","%"+" "+top3+" "+"%","%"+" "+top1+" "+"%",\
	"%"+" "+top2+" "+"%","%"+" "+top3+" "+"%"])
	
	TopWords_len = len(TopWords.fetchall())
	#print "TopWords_len",TopWords_len
		
	conn.commit()
	conn.close()
			
	if TopWords_len > 0:
		ergebnis = list(ergebnis)
		#print "Ergebnis: ",ergebnis
		satz = ergebnis[0]
	if TopWords_len == 0:
		#print "0"
		ergebnis = "Chappy weiss das noch nicht."
		satz = ergebnis
		return ergebnis


	response_predecessor.append(satz)
	response_successor.append(satz)

# schleife solange bis abbruchsymbol

	def search_predecessor_chain(satz):
		'''suche nach einem vorgaenger Satz'''
		
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
		#print "Neuer Satz: ",neuerSatz

		#try:
		for row in c.execute('SELECT kette, probability FROM Kette WHERE\
		(kette like ?) AND NOT (kette like ?) ORDER BY probability DESC limit 1 ',["%"+neuerSatz+"%","%"+satz+"%"]):
			ergebnis = row
		
		predecessor_anfrage = c.execute('SELECT kette, probability FROM Kette WHERE\
		(kette like ?) AND NOT (kette like ?) ORDER BY probability DESC limit 1 ',["%"+neuerSatz+"%","%"+satz+"%"])
		predecessor_anfrage_len = len(predecessor_anfrage.fetchall())
		print "Predecessor_len: ",predecessor_anfrage_len
		
		conn.commit()
		conn.close()

		if predecessor_anfrage_len > 0:
			ergebnis = list(ergebnis)
			ergebnis = ergebnis[0]

			vorgaenger_wort = ergebnis.split(" ")
			#print "Vorgaenger Ergebnis: ",ergebnis

			response_predecessor.insert(0,vorgaenger_wort[0])

			if "." in vorgaenger_wort[-1]:
				print "Vorheriger Satz erkannt! Beginne hier:"
			else:
				search_predecessor_chain(ergebnis)
		if predecessor_anfrage_len == 0:
			print "kein Vorgaenger"

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
		#print neuerSatz
		try:
			''' to do: vernueftige fehlerbehandlung! wenn kein ergebnis mehr vorliegt was dannmachen?'''
			for row in c.execute('SELECT kette, probability FROM Kette WHERE \
			(kette like ?) AND NOT (kette like ?) ORDER BY probability DESC limit 1 ',["%"+neuerSatz+"%","%"+satz+"%"]):
				ergebnis = row

			ergebnis = list(ergebnis)
			ergebnis = ergebnis[0]
			conn.commit()
			conn.close()

			nachfolger_wort = ergebnis.split(" ")
			#print "Nachfolger Ergebnis: ",ergebnis
			regex = "."
			try:
				response_successor.append(nachfolger_wort[-1])
			except: 
				pass
			#print "nachfolger_wort[-1]" +nachfolger_wort[-1]
			if "." in nachfolger_wort[-1]:
				print "Found END of Sentence"
			else:
				search_successor_chain(ergebnis)
		except:
			pass

	search_predecessor_chain(satz)
	search_successor_chain(satz)

	print "predecessor: ",response_predecessor
	response_predecessor_finish = []
	
	'''to do: ueberlegen was passiert wenn erster Satz (findet keinen punkt)
		andere option fuer fehlerabfrage ueberlegen anstatt try except
	'''
	try:
		for item in response_predecessor:
			#print "Item:",item
			if "." in item:
				index_dot = response_predecessor.index(item)
				print "index_dot: ",index_dot
	except:
		pass
	# endgueltige vorgaengerliste bekommt vorganger uebergeben, wenn es
	# einen gibt
	try:
		for item in range(index_dot,len(response_predecessor)):
			response_predecessor_finish.append(response_predecessor[item])
	except:
		pass
	try:
		response_predecessor = response_predecessor[-1] #[-1] damit es keine doppelten worte gibt
		response_successor = response_successor[1:] #[1:] damit es keine doppelten worte gibt
		response_successor = ' '.join(response_successor) # umwandlung zum string
		response_predecessor = ' '.join(str(element) for element in response_predecessor_finish)
		response_predecessor = response_predecessor.split('.',1)[1]
	except:
		pass
	# vorgaenger und nachfolger werden zu einem Satz
	response = response_predecessor+" "+response_successor
	print "predecessor: ",response_predecessor
	print "sucessor: ",response_successor
	return response

if __name__ == "__main__":
	
	top_3_words = get_top_entropies("whats going it")
	#top_3_words = get_top_entropies("is")
	search_for_keyword(top_3_words)

