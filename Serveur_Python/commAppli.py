#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify, session
import requests
import json
from mongoengine import *
import sys
import datetime
from protege import rest_api
sys.path.append('../BDD')
import tables

app = Flask(__name__)
db_connec = connect('GHome_BDD')
app.secret_key = '\xdf\x0e4\xaa\xdb:\xa8\xc6\r\x14\x96|\xc56\xfaq=\xb3\xb9\xc6\xaf\xab\x7fe'
app.register_blueprint(rest_api)

# \ ! / Monkey patching mongoengine to make json dumping easier
Document.to_dict = lambda s : json.loads(s.to_json())

def etat_to_tuples(piece_id):
	etat = tables.Etat.objects(piece_id=piece_id).first()
	piece = tables.Piece.objects(piece_id=piece_id).first()
	rid = "Fermés"
	if etat.rideauxOuverts : rid = "Ouverts"

	inc = "Non déclenchée"
	if etat.antiIncendieDeclenche : inc = "Déclenchée"

	clim = "Eteinte"
	if etat.climActivee : rid = "Active"

	vol = "Fermés"
	if etat.voletsOuverts : vol = "Ouverts"

	prise = "Fermés"
	if etat.priseDeclenchee : prise = "Ouverts"

	result = { "couples": [ { "image" : "hotel.png", "width" : "40px", "nom":"Piece" , "valeur": piece.name },
							{ "image" : "temp.png", "width" : "30px","nom":"Température" , "valeur": etat.temperature },
							{ "image" : "hum.png", "width" : "20px","nom":"Humidité" , "valeur": etat.humidite },
							{ "image" : "rideaux.png", "width" : "30px","nom":"Rideaux" , "valeur": rid },
							{ "image" : "hotel.png", "width" : "40px","nom":"Climatisation" , "valeur": piece.name },
							{ "image" : "hotel.png", "width" : "40px","nom":"Prise intelligente" , "valeur": prise },
							{ "image" : "fire.png", "width" : "30px","nom":"Antincendie" , "valeur": inc },
							{ "image" : "hotel.png", "width" : "40px","nom":"Volets" , "valeur": vol }
							]
			}
	return result

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/surveillance')
def surveillance():
    return render_template('surveillance.html')

@app.route('/controle')
def controle():
    return render_template('controle.html')

@app.route('/parametrage')
def parametrage():
    return render_template('parametrage.html')

@app.route('/surveillance/pieces')
def get_pieces():
	pieces = [p.to_dict() for p in tables.Piece.objects.order_by('+piece_id')]
	reponse = dict(ok=True, result=pieces)
	return json.dumps(reponse)

@app.route('/surveillance/personnages')
def get_persos():
	piece_id = request.args.get('piece')
	piece_id = int(piece_id)
	etat = tables.Etat.objects(piece_id=piece_id).first()
	persos = [p.to_dict() for p in etat.persosPresents]
	reponse = dict(ok=True, result=persos)
	return json.dumps(reponse)

@app.route('/surveillance/etat/<piece_id>')
def get_etat_piece(piece_id):
	etat = etat_to_tuples(piece_id)
	return json.dumps(etat)

@app.route('/controle/<piece_id>')
def get_actionneurs(piece_id):
	piece = tables.Piece.objects(piece_id=piece_id).first()
	actionneurs = [a.to_dict() for a in piece.actionneurs]
	return jsonify(ok=True, result=actionneurs)

@app.route('/controle/action')
def send_action():
	id_act = request.args.get('action')
	piece = request.args.get('piece')
	act_type = request.args.get('type')
	print str(id_act)
	now = datetime.datetime.now()
	reponse = tables.DonneeAppli(date=now,piece_id=piece,actionneur_id=id_act,action_type=act_type)
	reponse.save()
	return "ok"

@app.route('/surveillance/<perso_id>')
def ignore(perso_id):
	perso = tables.Personne.objects(personne_id=perso_id).first()
	perso.ignore = True
	perso.save()
	return "ok"

@app.route('/surveillance/reponse')
def reponse():
	rep = request.args.get('rep')
	nom = request.args.get('piece')
	piece = tables.Piece.objects(name=nom).first()
	now = datetime.datetime.now()
	reponse = tables.ReponseAppli(date=now,piece_id=piece.piece_id,reponse=False)
	if rep == 'oui' :
		reponse.ReponseAppli = True	
	reponse.save()
	return "ok"

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html', error=False)

@app.route('/login', methods=['POST'])
def process_login():
    name, password = request.form['username'], request.form['password']
    user = tables.Personne.objects(nom=name).first()
    if user is None :
        app.logger.warning("Couldn't login : {}".format(user))
        return render_template('login.html', error=True, username=name)
    else:
        session['logged_in'] = user.nom
    return redirect('/')

@app.context_processor
def inject_user():
    """ Injects a 'user' variable in templates' context when a user is logged in """
    if session.get('logged_in', None):
        return dict(user=tables.Personne.objects.get(nom=session['logged_in']))
    else:
        return dict(user=None)

if __name__ == '__main__':
    app.run(debug=True)
