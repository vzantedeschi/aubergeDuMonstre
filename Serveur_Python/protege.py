#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import mongoengine

from flask import request, session, jsonify, Blueprint, g
sys.path.append('../BDD')
import tables

rest_api = Blueprint('rest_api', __name__)

@rest_api.before_request
def load_user():
    """ Injects the current logged in user (if any) to the request context """
    g.user = tables.Personne.objects(nom=session.get('logged_in')).first()