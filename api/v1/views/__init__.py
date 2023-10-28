#!/usr/bin/python3
""" Init file for views module """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from api.v1.views.index import *
