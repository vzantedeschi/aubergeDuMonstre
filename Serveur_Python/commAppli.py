#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify, session
import requests
import json
from mongoengine import *
import sys
import datetime
sys.path.append('../BDD')
import tables

app = Flask(__name__)
db_connec = connect('GHome_BDD')
app.secret_key = '\x11\x7f\xa7\xd8\xb6\xac\x83[=O@\x9c\x89\x0b\x13Y\x16\xcb\xf9\xcd<c\xdc\x12'

### fonction de conversion des instances mongoengine en dictionnaires json ###
Document.to_dict = lambda s : json.loads(s.to_json())

def etat_to_tuples(piece_id):
	etat = tables.Etat.objects(piece_id=piece_id).first()
	piece = tables.Piece.objects(piece_id=piece_id).first()
	
	rid = "Fermés"
	if etat.rideauxOuverts : rid = "Ouverts"

	inc = "Non déclenchée"
	if etat.antiIncendieDeclenche : inc = "Déclenchée"

	clim = "Eteinte"
	if etat.climActivee : clim = "Active"

	vol = "Fermés"
	if etat.voletsOuverts : vol = "Ouverts"

	prise = "Eteinte"
	if etat.priseDeclenchee : prise = "Active"

	result = { "couples": [ { "image" : "hotel.png", "width" : "40px", "nom":"Piece" , "valeur": piece.name , "title" : True},
							{ "image" : "temp.png", "width" : "30px","nom":"Température" , "valeur": etat.temperature },
							{ "image" : "hum.png", "width" : "20px","nom":"Humidité" , "valeur": etat.humidite },
							{ "image" : "rideaux.png", "width" : "30px","nom":"Rideaux" , "valeur": rid },
							{ "image" : "hotel.png", "width" : "40px","nom":"Climatisation" , "valeur": clim },
							{ "image" : "hotel.png", "width" : "40px","nom":"Prise intelligente" , "valeur": prise },
							{ "image" : "fire.png", "width" : "30px","nom":"Antincendie" , "valeur": inc },
							{ "image" : "hotel.png", "width" : "40px","nom":"Volets" , "valeur": vol }
							]
			}
	return result

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', None):
            return render_template('login.html', warn=True)
        else:
            return f(*args, **kwargs)
    return decorated_function

def requires_admin_rights(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', None):
            return render_template('login.html', warn=True)
        elif session['logged_in'] != 'administrateur':
        	return redirect('/')
        else :
            return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    if session.get('logged_in', None):
        return dict(user=tables.Utilisateur.objects.get(identifiant=session['logged_in']))
    else:
        return dict(user=None)

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html', error=False, warn=False)

@app.route('/login', methods=['POST'])
def process_login():
    ident, mot = request.form['username'], request.form['password']
    user = tables.Utilisateur.objects(identifiant=ident).first()
    if user is None or user.valider_mot_passe(mot):
        app.logger.warning("Impossible de se logger : {}".format(user))
        return render_template('login.html', error=True, username=ident)
    else:
        session['logged_in'] = user.identifiant
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/surveillance')
@requires_login
def surveillance():
    return render_template('surveillance.html')

@app.route('/controle')
@requires_login
def controle():
    return render_template('controle.html')

@app.route('/parametrage', methods=['GET'])
@requires_admin_rights
def parametrage():
    return render_template('parametrage.html')

@app.route('/parametrage', methods=['POST'])
@requires_admin_rights
def send_parametrage():
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
	logged = session.get('logged_in', None)
	reponse = dict(ok=True, result=persos, logged=str(logged))
	return json.dumps(reponse)

@app.route('/surveillance/etat/<piece_id>')
def get_etat_piece(piece_id):
	etat = etat_to_tuples(piece_id)
	return json.dumps(etat)

@app.route('/controle/<piece_id>')
def get_actionneurs(piece_id):
	piece = tables.Piece.objects(piece_id=piece_id).first()
	actionneurs = [a.to_dict() for a in piece.actionneurs]
	return jsonify(ok=True, result=actionneurs, piece=piece.name)

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
		reponse.reponse = True
	reponse.save()
	return "ok"

@app.route('/add/capteur')
@requires_login
def add_capteur():
	pieces = [p.name for p in tables.Piece.objects()]
	types = set([c.capteur_type for c in tables.Capteur.objects()])
	return render_template('capteur.html', pieces=pieces, types=types)

@app.route('/add/actionneur')
@requires_login
def add_actionneur():
	pieces = [p.name for p in tables.Piece.objects()]
	types = set([c.capteur_type for c in tables.Actionneur.objects()])
	return render_template('actionneur.html', pieces=pieces, types=types)

if __name__ == '__main__':
    app.run(debug=True)
