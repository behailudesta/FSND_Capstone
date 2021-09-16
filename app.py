import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from werkzeug.wrappers import response
from models import setup_db, Actors, Movies, Performances

def create_app(test_config=None):
  # create and configure the app

  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  return app

APP = create_app()



if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)
 