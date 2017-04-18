'''
- Startsymbol !$!
- Endsymbol !€!

Finde bestmögliche Antwort aus DB

'''
import sqlite3
import re
import time


def get_top_entropies(input):
	print("------------------------------")
	print("Hole die Entropie...")
	print("------------------------------")
	user_input = input.split(" ")	
	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()
	
	top_entropie_words = []
	for element in user_input:
		for ausgabe in c.execute('SELECT wort,entropy FROM Entropy \
		WHERE wort = "'+element+'" ORDER BY entropy DESC limit 1'):
			
			print("sql Entropy: ",ausgabe)
		cursor = c.execute('SELECT wort,entropy FROM Entropy \
		WHERE wort = "'+element+'" ORDER BY entropy DESC limit 1')
		cursor_len = len(cursor.fetchall())
		
		if cursor_len > 0:
			ausgabe = list(ausgabe)
			top_entropie_words.append(ausgabe)
		
		'''sortiert die Liste nach ihrer Entropy'''
	top_entropie_words.sort(key = lambda row: row[1])

	top_3_words = top_entropie_words[0:3]
	top_3_words = [item[0] for item in top_3_words]
	print("------------------------------")
	print("Top 3 Entropie ermittelt: ",top_3_words)
	print("------------------------------")
	'''
	-top drei keywords sollen beachtet werden
	-es sollen die keywords mit der besten entropie(niedrigster wert) 
	genommen werden
	-dann soll ein satz der das beste keyword enthaelt ausgegeben werden
	'''
	conn.commit()
	conn.close()
	
	return top_3_words
	
'''Keywordsuche zum ausgeben des wahrscheinlichsten Satzes'''
def search_for_keyword(top_3_words):
	print("----------------------------------")
	print("Berechne bestmögliche Antwort...")
	print("----------------------------------")
	response_predecessor = []
	response_successor = []

	conn = sqlite3.connect("chappies_brain.db")
	c = conn.cursor()

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
	
	print("1. = ",top1)
	print("2. = ",top2) 
	print("3. = ",top3)

	for row in c.execute('SELECT kette, probability FROM Kette \
	WHERE \
	   (kette like ? AND kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ? AND kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	OR (kette like ?)\
	ORDER BY probability DESC limit 1',
	["%"+" "+top1+" "+"%","%"+" "+top2+" "+"%","%"+" "+top3+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top2+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top3+" "+"%","%"+" "\
	+top2+" "+"%","%"+" "+top3+" "+"%","%"+" "+top1+" "+"%",\
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
	ORDER BY probability DESC limit 1',["%"+" "+top1+" "+"%","%"+" "\
	+top2+" "+"%","%"+" "+top3+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top2+" "+"%",\
	"%"+" "+top1+" "+"%","%"+" "+top3+" "+"%","%"+" "+top2+" "+\
	"%","%"+" "+top3+" "+"%","%"+" "+top1+" "+"%",\
	"%"+" "+top2+" "+"%","%"+" "+top3+" "+"%"])
	
	TopWords_len = len(TopWords.fetchall())
		
	conn.commit()
	conn.close()
			
	if TopWords_len > 0:
		ergebnis = list(ergebnis)

		satz = ergebnis[0]
	if TopWords_len == 0:

		ergebnis = "Chappy weiss das noch nicht." # To do: Lieber eine Auswahl von Sätzen random ausgeben / Täuschung des Nutzers
		satz = ergebnis
		return ergebnis


	response_predecessor.append(satz)
	response_successor.append(satz)
	print("----------------------------------")
	print("Antwort PREDECESSOR: ",response_predecessor)
	print("Antwort SUCCESSOR: ",response_successor)
	print("----------------------------------")



	def search_predecessor_chain(satz):
		print("")
		print("----------------Berechne Vorgänger----------------")
		print("")
		'''suche nach einem vorgaenger Satz'''
		conn = sqlite3.connect("chappies_brain.db")
		c = conn.cursor()

		satzsplit = satz.split(" ")
		neuerSatz = []
		for word in range(len(satzsplit)-1):
			try:
				neuerSatz.append(satzsplit[word])
			except: 
				pass
		neuerSatz = ' '.join(neuerSatz)
		
		predecessor_anfrage = c.execute('SELECT kette, \
		probability FROM Kette WHERE\
		(kette like ?) AND NOT \
		(kette like ?) ORDER BY probability \
		DESC limit 1 ',["%"+neuerSatz+"%","%"+satz+"%"])
		
		result = predecessor_anfrage.fetchall()
		len_result = len(result)
		conn.commit()
		conn.close()
		print("----------------------------------")
		print("DB Ergebnis Predeccessor:",result)
		print("----------------------------------")
		result = ([x[0] for x in result])
		
		if len(result) > 0:
			result = result[0]
			vorgaenger_wort = result.split(" ")
			print("Vorgaenger Ergebnis: ",result)
			response_predecessor.insert(0,vorgaenger_wort[0])
			print(response_predecessor,result)
			if "!$!" in result:
				print("Vorheriger Satz erkannt! Beginne hier:")
			else:
				print("Satzanfang noch nicht gefunden, suche weiter!")
				if len(response_predecessor) > 3 and \
				response_predecessor[0] == response_predecessor[1] \
				== response_predecessor[2]:
					print("----------------------------------")
					print("len > 3 Endlosschleife entdeckt, beende \
					Suche nach Satzanfang!")
					print("----------------------------------")
					# to do: und dann? Fallback Lösung:
					# Auswahl von vorgefertigten Sätzen?

				else:
					search_predecessor_chain(result)
		if len_result == 0:
			print("----------------------------------")
			print("Kein Vorgaenger gefunden!")
			print("----------------------------------")

	def search_successor_chain(satz):
		print("")
		print("----------------Berechne Nachfolger----------------")
		print("")
		conn = sqlite3.connect("chappies_brain.db")
		c = conn.cursor()
		
		satzsplit = satz.split(" ")
		neuerSatz = []
		for word in range(len(satzsplit)):
			try:
				neuerSatz.append(satzsplit[word+1])
			except: 
				pass
		neuerSatz = ' '.join(neuerSatz)
		
		successor_anfrage = c.execute('SELECT kette, \
		 probability FROM Kette WHERE\
		(kette like ?) AND NOT (kette like ?) ORDER BY \
		probability DESC limit 1 ',[neuerSatz+"%","%"+satz+"%"])
		
		result = successor_anfrage.fetchall()
		len_result = len(result)
		
		conn.commit()
		conn.close()
		print("----------------------------------")
		print("DB Ergebnis Successor:",result)
		print("----------------------------------")
		result = ([x[0] for x in result])
			
		if len(result) > 0:
			result = result[0]
			print("ERGEBNIS SUCC", result)
			nachfolger_wort = result.split(" ")
			print("Nachfolger Ergebnis: ",result)
			response_successor.append(nachfolger_wort[-1])
			print("nachfolger_wort[-1]",nachfolger_wort[-1])
			if "!€!" in nachfolger_wort:
				print("Satzende gefunden!")
			else:
				search_successor_chain(result)

	search_predecessor_chain(satz)
	search_successor_chain(satz)
	print("predecessor: ",response_predecessor)
	response_predecessor_finish = []
	
	for item in response_predecessor:
		print("Item:",item)
		if "!$!" in item:
			index_dot = response_predecessor.index(item)
			print("index_dot: ",index_dot)

	try:
		for item in range(index_dot,len(response_predecessor)):
			response_predecessor_finish.append(\
			response_predecessor[item])
	except:
		print("Fehler! Weil")
	try:
		response_predecessor = response_predecessor[-1]
		""" [-1] damit es keine doppelten worte gibt """
		response_successor = response_successor[1:]
		""" [1:] damit es keine doppelten worte gibt """
		response_successor = ' '.join(response_successor)
		""" umwandlung zum string """
		response_predecessor = ' '.join(str(element) for element in \
		response_predecessor_finish)
		response_predecessor = response_predecessor.split('.',1)[1]
	except:
		print("Fehler beim Zusammenführen von Vorgänger und Nachfolger")
		
	""" vorgaenger und nachfolger werden zu einem Satz """
	response = response_predecessor+" "+response_successor
	print("predecessor: ",response_predecessor)
	print("sucessor: ",response_successor)
	print("RESPONSE: ", response)
	return response

if __name__ == "__main__":
	""" Helper Function / Debugging """
	#top_3_words = get_top_entropies("i want an quite intense wine")
	#top_3_words = get_top_entropies("mineral palate")
	top_3_words = get_top_entropies("wine excellent")
	#top_3_words = get_top_entropies("pretty good")
	search_for_keyword(top_3_words)

