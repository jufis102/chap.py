from flask import Flask, jsonify, render_template, request
from search_for_keyword import search_for_keyword, get_top_entropies
from create_corpus import write_to_corpus, create_marcov_chain, tokenize_sentences
from create_entropy import create_entropy
from create_probabilities import calculate_probability, drop_probability
import sqlite3
import threading
import time
app = Flask(__name__)

app.debug = True

# initialisiere Lernvorgang
def init_learning(input_text):
    sentences = tokenize_sentences(input_text)
    marcov_chain = create_marcov_chain(sentences)
    print("MARCOV_CHAIN",marcov_chain)
    write_to_corpus(marcov_chain)

    #drop_probability()  # delete old probabilities
    #calculate_probability() # calculate new probabilites
    
    #create_entropy()

@app.route('/get_user_input', methods=["GET","POST"])
def get_user_input():
    input = request.args.get('input', type=str)
    input = input.lower()    
    output = get_top_entropies(input)
    output = search_for_keyword(output)
    init_learning(input)
    
    
    return jsonify(result=output,input=input)

@app.route('/')
def index():
    return render_template('index.html')

def learning_routine():
	start_time=time.clock()
	calculate_probability()
	create_entropy()
	end_time=time.clock()
	a_time=end_time-start_time
	print(a_time)


	



if __name__ == "__main__":
	app.run(host='0.0.0.0')

# packages in folder: usr/lib/python3.5/dist_packages
