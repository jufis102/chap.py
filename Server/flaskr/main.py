from flask import Flask, jsonify, render_template, request
from search_for_keyword import search_for_keyword, get_top_entropies
from create_corpus import write_to_corpus, create_marcov_chain, tokenize_sentences
from create_entropy import create_entropy
from create_probabilities import calculate_probability, drop_probability
import sqlite3
app = Flask(__name__)

app.debug = True

# initialisiere Lernvorgang
def init_learning(input_text):
    sentences = tokenize_sentences(input_text)
    marcov_chain = create_marcov_chain(sentences)
    print("MARCOV_CHAIN",marcov_chain)
    write_to_corpus(marcov_chain)

    drop_probability()  # delete old probabilities
    calculate_probability() # calculate new probabilites
    
    create_entropy()

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


@app.route('/admintool',methods=["GET","POST"])
def admintool():

    if 'submit_text' in request.form:
        input_text = request.form['input_text']
        #print input_text
        input_text = input_text#.decode('utf-8')
        init_learning(input_text)
        #print type(input_text)
        #marcov_chain = create_marcov_chain(input_text)
        #write_to_corpus(marcov_chain)
        #calculate_probability()
        #create_entropy()
        
    if 'delete_db' in request.form:
            conn = sqlite3.connect("chappies_brain.db")
            c = conn.cursor()

            c.execute("DELETE from corpus")
            c.execute("DELETE from kette")
            c.execute("DELETE from entropy")
            conn.commit()
            conn.close()
            print("loesche db...")

    return render_template('admintool.html')



if __name__ == "__main__":
	app.run(host='0.0.0.0')

# packages in folder: usr/lib/python3.5/dist_packages
