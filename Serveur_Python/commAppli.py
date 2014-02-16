#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
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

@app.route('/surveillance/etats')
def get_etats():
	etats = [e.to_dict() for e in tables.Etat.objects.order_by('+piece_id')]
	reponse = dict(ok=True, result=etats)
	return json.dumps(reponse)

if __name__ == '__main__':
    app.run(debug=True)
