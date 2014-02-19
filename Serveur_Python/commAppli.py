#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import requests
import json
from mongoengine import *
import sys
sys.path.append('../BDD')
import tables

app = Flask(__name__)
db_connec = connect('GHome_BDD')

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

@app.route('/controle', methods=['GET', 'POST'])
def controle():
    return render_template('controle.html')

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
	return json.dumps(actionneurs)


"""@app.route('/surveillance/<perso_id>')
def ignore(perso_id):
	perso = tables.Personne.objects(personne_id=perso_id).first()
	print "avant " + str(perso.ignore)
	perso.ignore = True
	print "après " + str(perso.ignore)
	perso.save()
	return "ok"""

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html', error=False)

@app.route('/login', methods=['POST'])
def process_login():
    """email, password = request.form['email'].lower(), request.form['password']
    user = User.objects(email=email).first()
    if user is None or not user.valid_password(password):
        app.logger.warning("Couldn't login : {}".format(user))
        return render_template('login.html', error=True, email=email)
    else:
        session['logged_in'] = user.email"""
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
