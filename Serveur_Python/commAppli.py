#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify, session
import json
import time
from mongoengine import *
import sys
import datetime
sys.path.append('../BDD')
import tables

app = Flask(__name__)
db_connec = connect('GHome_BDD', host='192.168.137.1')
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

    portes = "Ouvertes"
    if etat.portesFermees : portes = "Fermées"

    result = { "couples": [ { "image" : "hotel.png", "width" : "40px", "nom":"Piece" , "valeur": piece.name , "title" : True},
                            { "image" : "temp.png", "width" : "30px","nom":"Température" , "valeur": etat.temperature },
                            { "image" : "hum.png", "width" : "20px","nom":"Humidité" , "valeur": etat.humidite },
                            { "image" : "rideaux.png", "width" : "30px","nom":"Rideaux" , "valeur": rid },
                            { "image" : "clim.png", "width" : "30px","nom":"Climatisation" , "valeur": clim },
                            { "image" : "prise.png", "width" : "30px","nom":"Prise intelligente" , "valeur": prise },
                            { "image" : "fire.png", "width" : "30px","nom":"Antincendie" , "valeur": inc },
                            { "image" : "portes.png", "width" : "40px","nom":"Portes" , "valeur": portes },
                            { "image" : "volets.png", "width" : "30px","nom":"Volets" , "valeur": vol }
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
    if user is None or not user.valider_mot_passe(mot):
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
	retour = request.form.getlist("regle")
	for a in retour:
		tables.Regle.objects(regle_id=a).first().delete()
		print a
	return render_template('parametrage.html')

@app.route('/parametrage/chargerRegles')
@requires_admin_rights
def get_regles():
    listeRegles = [p.to_dict() for p in tables.Regle.objects]
    reponse = dict(ok=True, result=listeRegles)
    return json.dumps(reponse)

@app.route('/parametrage/ActCond/<regle_id>')
@requires_admin_rights
def get_actCond(regle_id):
    regle = tables.Regle.objects(regle_id=regle_id).first()
    actions = [p.to_dict() for p in regle.actions]
    conditions = [a.to_dict() for a in regle.conditions]
    reponse=dict(ok=True, actions=actions, conditions=conditions, id_regle=regle_id)
    return json.dumps(reponse)

@app.route('/ajoutRegle', methods=['GET', 'POST'])
@requires_admin_rights
def ajoutRegle():
    return render_template('ajoutRegle.html')

@app.route('/ajoutRegle/chargerCond')
@requires_admin_rights
def sendCond():
	listeCond = [c.to_dict() for c in tables.ConditionGenerique.objects]
	reponse = dict(ok=True, result=listeCond)
	return json.dumps(reponse)

@app.route('/ajoutRegle/chargerAct')
@requires_admin_rights
def sendAct():
	listeAct = [a.to_dict() for a in tables.Action.objects]
	reponse = dict(ok=True, result=listeAct)
	return json.dumps(reponse)

@app.route('/ajoutRegle/creer', methods=['POST'])
@requires_admin_rights
def creation():
	retourCond = request.form.getlist("condition")
	if retourCond==[]:
		#les champs sont incomplets
		return redirect('/ajoutRegle')
	else :
		retourAct = request.form.getlist("action")
		if retourAct==[]:
			#les champs sont incomplets
			return redirect('/ajoutRegle')
		else:
			nom = request.form.get('nomRegle')
			if nom == "":
				#les champs sont incomplets
				return redirect('/ajoutRegle')
			else:
				conditions = tables.ConditionGenerique.objects(nom__in=retourCond)
				newConds = []
				for cond in conditions:
					if cond.nom in ["tempSup", "tempInf", 'humInf', 'humSup', 'pasBouge', 'pasChange']:
						val = request.form.get(cond.nom)
						newCond = tables.Condition(nom=cond.nom, valeur=val, description=cond.description)
					else:
						newCond = tables.Condition(nom=cond.nom, description=cond.description)
					newCond.save()
					newConds.append(newCond)
				
				actions = tables.Action.objects(nom__in=retourAct)
				
				listeIdRegles = [r.regle_id for r in tables.Regle.objects]
				maxid = max(listeIdRegles) + 1

				regle = tables.Regle( regle_id= maxid, nom = nom, conditions = newConds, actions = actions)
				regle.save()
				return redirect('/parametrage')

@app.route('/modifierRegle')
@requires_admin_rights
def modifierRegle():
    return render_template('modifierRegle.html')

@app.route('/modifierRegle/<id_regle>')
@requires_admin_rights
def modifierRegleId(id_regle):
    regle = tables.Regle.objects(regle_id=id_regle).first()
    conds = []
    for cond in regle.conditions:
        if cond.valeur != None:
            conds.append(cond.to_dict())

    reponse = dict(ok=True, result=conds)
    return json.dumps(reponse)
    
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
	id_act = int(request.args.get('action'))
	piece = int(request.args.get('piece'))
	act_typeStr = request.args.get('type')
	act_type = False
	if act_typeStr == 'true':
		act_type = True
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

@app.route('/appareillage/capteur')
@requires_login
def appareillage_capt():
	id = int(request.args.get('id'),16)
	type = request.args.get('type')
	piece = tables.Piece.objects.get(name=request.args.get('piece')).piece_id
	now = datetime.datetime.now()
	reponse = tables.DemandeAppareillage(date=now,piece_id=piece,ident=id,dispositif='Capteur',type=type)
	reponse.save()
	time.sleep(10)
	conf = tables.ConfirmationAppareillage.objects(ident=id)
	if conf :
		return jsonify(error=False)
	else :
		reponse = tables.DemandeAppareillage(date=now,piece_id=piece,ident=id,dispositif='Capteur',type=type, creer=False)
		reponse.save()
		return jsonify(error=True)

@app.route('/appareillage/actionneur')
@requires_login
def appareillage_act():
    id = int(request.args.get('id'),16)
    type = request.args.get('type')
    piece = tables.Piece.objects.get(name=request.args.get('piece')).piece_id
    now = datetime.datetime.now()
    reponse = tables.DemandeAppareillage(date=now,piece_id=piece,ident=id,dispositif='Actionneur',type=type)
    reponse.save()
    return jsonify(error=False)

@app.route('/appareillage/verifier')
@requires_login
def verifierID():
	id = request.args.get('id')
	if id == '' or tables.Capteur.objects(capteur_id=id) or tables.Actionneur.objects(actionneur_id=id):
		return jsonify(error=True)
	else:
		return jsonify(error=False)

@app.route('/appareillage/annuler')
@requires_login
def annuler():
    id = int(request.args.get('id'),16)
    type = request.args.get('type')
    piece = tables.Piece.objects.get(name=request.args.get('piece')).piece_id
    now = datetime.datetime.now()
    reponse = tables.DemandeAppareillage(date=now,piece_id=piece,ident=id,dispositif='Actionneur',type=type, creer=False)
    reponse.save()
    return 'ok'


@app.route('/appareillage/confirmer')
@requires_login
def confirmer():
    id = int(request.args.get('id'),16)
    piece = tables.Piece.objects.get(name=request.args.get('piece')).piece_id
    now = datetime.datetime.now()
    actionneur = tables.Actionneur.objects(actionneur_id = id).first()
    actionneur.interpreter = True;
    actionneur.save();
    conf = tables.ConfirmationAppareillage(piece_id = piece.piece_id, date = now, traite = True,ident=id)
    conf.save()
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
