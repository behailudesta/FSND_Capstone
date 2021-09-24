from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()

class Movies(db.Model):
    __tablename__ = 'Movies'

    #id = db.Column(Integer, primary_key=True, nullable = False)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    # one-to-may to the Show table/Model
    Performances = db.relationship('Performances', backref='Movies', lazy = True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date

    }

    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}>'

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
     
    # many-to-many to the Show table/Model
    Performances = db.relationship('Performances', backref='Actors', lazy = True)
    
    def __repr__(self):
        return f'<Actors ID: {self.id}, name: {self.name}, age: {self.age}, gender : {self.gender}>'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }

class Performances(db.Model):
    __tablename__ = 'Performances'
    # foreign key(primary keys of Movie and Actors tables/Models)
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable = False)
    actors_id = db.Column(db.Integer, db.ForeignKey('Actors.id'), nullable = False)
    character = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Performances ID : {self.id}, movies_id: {self.movies_id}, actors_id: {self.actors_id}>'

