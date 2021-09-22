import os
from flask_cors import CORS
import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort , jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from werkzeug.wrappers import response
from models import * #setup_db, Actors, Movies, Performances


ITEMS_PER_PAGE = 10

'''
  Paginate Movies
'''
def paginate_movies(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1)* ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  movies = [Movies.format() for Movies in selection]
  current_movies = movies[start:end]

  return current_movies

'''
  Paginate Actors
'''
def paginate_actors(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1)* ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  actors = [Actors.format() for Actors in selection]
  current_actors = actors[start:end]

  return current_actors
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  #CORS Headers after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Headers', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def status():
    return jsonify({
      'status': 'Healthy running!!'
    }), 200

  '''
  An endpoint to handle GET requests for all available Movies.
  '''
  @app.route('/movies')
  def retrieve_movies():
    selection = Movies.query.order_by(Movies.id).all()
    current_movies = paginate_movies(request, selection)

    if len(current_movies) == 0:
      abort(404)

    return jsonify({
      'movies' : current_movies,
      'total_movies' : len(Movies.query.all()),
      'success' : True
    })

    
  '''
  An endpoint to handle GET requests for all available Actors.
  '''
  @app.route('/actors')
  def retrieve_actors():
    selection = Actors.query.order_by(Actors.id).all()
    current_actors = paginate_actors(request, selection)

    if len(current_actors) == 0:
          abort(404)

    return jsonify({
      'movies' : current_actors,
      'total_actors' : len(Actors.query.all()),
      'success' : True
    })

  '''
  DELETE a movie. 
  '''
  @app.route('/movies/<int:movies_id>', methods=['DELETE'])
  def delete_movies(movies_id):
    try:
      movies = Movies.query.filter(Movies.id == movies_id).one_or_none()
      
      if movies is None:
        abort(404)

      movies.delete()

      selection = Movies.query.order_by(Movies.id).all()
      current_movies = paginate_movies(request,selection)
      
      return jsonify({
        'success' : True,
        'deleted' : movies_id,
        'movies' : current_movies,
        'totalMovies' : len(Movies.query.all())
      })
    #except unprocessable:
    except :
      abort(422)

  '''
  DELETE an actor. 
  '''
  @app.route('/actors/<int:actors_id>', methods=['DELETE'])
  def delete_actors(actors_id):
    try:
      actors = Actors.query.filter(Actors.id == actors_id).one_or_none()
      
      if actors is None:
        abort(404)

      actors.delete()

      selection = Actors.query.order_by(Actors.id).all()
      current_actors = paginate_movies(request,selection)
      
      return jsonify({
        'success' : True,
        'deleted' : actors_id,
        'actors' : current_actors,
        'totalActors' : len(Actors.query.all())
      })
    #except unprocessable:
    except :
      abort(422)


  '''
  Post a movie. 
  '''
  @app.route('/movies', methods=['POST'])
  def create_new_movies():
    body = request.get_json()
    new_title = body.get('title',None)
    new_release_date = body.get('release_date',None)
    
    try:
      movies = Movies(title=new_title, release_date = new_release_date)
      movies.insert()

      selection = Movies.query.order_by(Movies.id).all()
      current_movies = paginate_movies(request,selection)

      return jsonify({
      'success' : True,
      'created' : movies.id,
      'movies' : current_movies,
      'totalMovies' : len(Movies.query.all())
    })   

    except :
       abort(422)

  '''
  Post an Actor. 
  '''
  @app.route('/actors', methods=['POST'])
  def create_new_actors():
    body = request.get_json()
    new_name = body.get('name',None)
    new_gender = body.get('gender',None)
    new_age = body.get('age',None)
    
    try:
      actors = Actors(name=new_name, gender = new_gender, age = new_age)
      actors.insert()

      selection = Actors.query.order_by(Actors.id).all()
      current_actors = paginate_actors(request,selection)

      return jsonify({
        'success' : True,
        'created' : actors.id,
        'movies' : current_actors,
        'totalMovies' : len(Actors.query.all())
        })   

    except :
       abort(422)  

  '''
  PATCH a Moive. 
  '''
  @app.route('/movies/<int:movies_id>', methods=['PATCH'])
  def update_movies(movies_id):
    body = request.get_json()

    try:
      movies = Movies.query.filter(Movies.id == movies_id).one_or_none()
      
      if movies is None:
        abort(404)
      if 'title' in body:
        movies.title = str(body.get('title'))
      if 'release_date' in body:
        movies.relese_date = body.get('relese_date')
      movies.update()

      return jsonify({
        'success': True
      })
    except:
      abort(400)
    
  '''
  PATCH an Actor. 
  '''
  @app.route('/actors/<int:actors_id>', methods=['PATCH'])
  def update_actors(actors_id):
    body = request.get_json()

    try:
      actors = Actors.query.filter(Actors.id == actors_id).one_or_none()
      
      if actors is None:
        abort(404)

      if 'name' in body:
        actors.name = str(body.get('name'))

      if 'gender' in body:
        actors.gender = body.get('gender')

      if 'age' in body:
            actors.age = body.get('age')
      
      actors.update()

      return jsonify({
        'success': True
      })
    except:
      abort(400)
 
    
  return app

APP = create_app()

if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)
 