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
    db.create_all()



class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

     # one-to-may to the Show table/Model
    Performances = db.relationship('Performances', backref='Movies', lazy = True)

    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}>'


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    #id = db.Column(db.Integer)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
     
    # many-to-many to the Show table/Model
    Performances = db.relationship('Performances', backref='Actors', lazy = True)
    
    def __repr__(self):
        return f'<Actors ID: {self.id}, name: {self.name}, age: {self.age}, gender : {self.gender}>'


class Performances(db.Model):
    __tablename__ = 'Performances'
    # foreign key(primary keys of Movie and Actors tables/Models)
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable = False)
    actors_id = db.Column(db.Integer, db.ForeignKey('Actors.id'), nullable = False)
    character = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Performances ID : {self.id}, movies_id: {self.movies_id}, actors_id: {self.actors_id}>'

