
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
from auth.auth import AuthError, requires_auth

# number of items per page for pagination
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
  
  '''
  Checking if web server is up and running. Status 200 OK
  '''

  @app.route('/')

  def status():
    return jsonify({
      'status': 'Healthy running!!'
    }), 200

  '''
  An endpoint to handle GET requests for all available Movies.
  '''
  @app.route('/movies')
  @requires_auth('get:movies')
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
  @requires_auth("get:actors")
  def retrieve_actors():
    selection = Actors.query.order_by(Actors.id).all()
    current_actors = paginate_actors(request, selection)

    if len(current_actors) == 0:
          abort(404)

    return jsonify({
      'actors' : current_actors,
      'total_actors' : len(Actors.query.all()),
      'success' : True
    })

  '''
  DELETE a movie. 
  '''
  @app.route('/movies/<int:movies_id>', methods=['DELETE'])
  @requires_auth("delete:movies")
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
  @requires_auth("delete:actors")
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
  @requires_auth("post:movies")
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

    except unprocessable:
       abort(422)

  '''
  Post an Actor. 
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth("post:actors")
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

    except unprocessable:
       abort(422)  

  '''
  PATCH a Moive. 
  '''
  @app.route('/movies/<int:movies_id>', methods=['PATCH'])
  @requires_auth("patch:movies")
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
  @requires_auth("patch:actors")
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
    except unprocessable:
      abort(400)
  '''
  Error handlers for all expected errors including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error": 422,
      "message": "unprocessable"
    }), 422
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
      }), 500
  
 
    
  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
  #app.run()
 