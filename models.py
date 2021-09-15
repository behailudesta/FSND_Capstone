

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

     # one-to-may to the Show table/Model
    Performances = db.relationship('Performances', backref='Movies', lazy = True)

    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}>'


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer(120))
    gender = db.Column(db.String(120))
     
    # many-to-many to the Show table/Model
    Performances = db.relationship('Performances', backref='Actors', lazy = True)
    
    def __repr__(self):
        return f'<Actors ID: {self.id}, name: {self.name}, age: {self.age}, gender : {self.gender}>'


class Performances(db.Model):
    __tablename__ = 'Performances'
    # foreign key(primary keys of Movie and Actors tables/Models)
    movies_id = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable = False)
    actors_id = db.Column(db.Integer, db.ForeignKey('Actors.id'), nullable = False)
    character = db.Column(db.string, nullable=True)

    def __repr__(self):
        return f'<Performances: {self.id}, startTime: {self.start_time}>'
