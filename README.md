# FSND-Capstone-Project
## Casting Agency API program

### Installing Dependencies 

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Models
Movies model defined with attributes title and release date.
Actors model defined with attributes name, age and gender.
You can find the models in models.py file. Local Postgres DATABASE details are available in setup.sh file for reference.

### Running the server

first ensure you are working using your created virtual environment.

    To run the server, execute:

    $ source setup.sh
    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
    $ flask run

## API Endpoints

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. An endpoint to handle GET requests for movies, including pagination (every 10 movies). This endpoint should return a list of movies, number of total movies. 


3. An endpoint to handle GET requests for actors, including pagination (every 10 actors). This endpoint should return a list of actors, number of total actors.


4. An endpoint to DELETE a movie using a moives ID. 


5. An endpoint to DELETE an actor using a actors ID. 


6. An endpoint to POST a new movie and actors. 


7. An endpoint to UPDATE an existing movie and actor. 


8. error handlers for all expected errors including 400, 404, 422 and 500. 

'''
API calls with example.

GET '/movies'

- Fetches a dictionary of movies
    Example:
    curl -X GET http://127.0.0.1:8080/movies

            "movies": [
                {
                "id": 2,
                "release_date": "Sat, 05 Sep 1998 08:00:00 GMT",
                "title": "Madagascar"
                },
                {
                "id": 3,
                "release_date": "Mon, 06 Feb 1989 08:00:00 GMT",
                "title": "Terminator"
                },
                {
                "id": 4,
                "release_date": "Mon, 01 Jan 1996 08:00:00 GMT",
                "title": "Titanic"
                },
                {
                "id": 5,
                "release_date": "Mon, 01 Jan 1990 08:00:00 GMT",
                "title": "Top Gun"
                },
                {
                "id": 6,
                "release_date": "Wed, 05 Jul 1989 08:00:00 GMT",
                "title": "The Merchant"
                }
            ],
            "success": true,
            "total_movies": 5
            }


```
GET '/actors'

    Example:
        curl -X GET http://127.0.0.1:8080/actors

            {
                "actors": [
                    {
                    "age": 66,
                    "gender": "Male",
                    "id": 1,
                    "name": "Johntra volta"
                    },
                    {
                    "age": 55,
                    "gender": "Male",
                    "id": 2,
                    "name": "Harrison Ford"
                    },
                    {
                    "age": 45,
                    "gender": "Female",
                    "id": 3,
                    "name": "Angelia Jolie"
                    }
                ],
                "success": true,
                "total_actors": 3
            }



DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
    
    Example:
    curl -X DELETE http://127.0.0.1:8080/movies/3
        {
            "deleted": 3,
            "success": true,
            "totalMovies": 6
        }

POST '/movies'
- Sends a post request in order to add a new movie

        Example:
        curl -X POST -H "Content-Type: application/json" -d '{"title":"Desperate Measures", "release_date":"01/01/1990"}' http://127.0.0.1:8080/movies
        {
                "created": 7,
                "movies": [
                    {
                    "id": 2,
                    "release_date": "Sat, 05 Sep 1998 08:00:00 GMT",
                    "title": "Madagascar"
                    },
                    {
                    "id": 3,
                    "release_date": "Mon, 06 Feb 1989 08:00:00 GMT",
                    "title": "Terminator"
                    },
                    {
                    "id": 4,
                    "release_date": "Mon, 01 Jan 1996 08:00:00 GMT",
                    "title": "Titanic"
                    },
                    {
                    "id": 5,
                    "release_date": "Mon, 01 Jan 1990 08:00:00 GMT",
                    "title": "Top Gun"
                    },
                    {
                    "id": 6,
                    "release_date": "Wed, 05 Jul 1989 08:00:00 GMT",
                    "title": "The Merchant"
                    },
                    {
                    "id": 7,
                    "release_date": "Mon, 01 Jan 1990 08:00:00 GMT",
                    "title": "Desperate Measures"
                    }
                ],
                "success": true,
                "totalMovies": 6
        }

    All the above Endpoints have been created, please refer app.py file.

###   Auth0 Setup

## API Endpoints
AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE are all available in the setup.sh file for reference. Json Web Tokens: You can find JWTs for each role in the setup.sh file to run the app locally.

Roles: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

    Casting Assistant * get:actors and get:movies
    Casting Director _ All permissions a Casting Assistant has and _ post:actors and delete:actors * patch:actors and patch:movies
    Executive Producer _ All permissions a Casting Director has and _ post:movies and delete:movies

### Deployment Details:
App is deployed to Heroku.
Heroku Postgres DATABASE details are available in setup.sh file for reference.
Use the above stated endpoints and append to this link above to execute the app either thru CURL or Postman. For example:

$ curl -X GET https://harsh-casting-agency.herokuapp.com//actors?page=1
$ curl -X POST https://harsh-casting-agency.herokuapp.com//actors
$ curl -X PATCH https://harsh-casting-agency.herokuapp.com//actors/1
$ curl -X DELETE https://harsh-casting-agency.herokuapp.com//actors/1

Similarly, you can build these for /movies endpoints too.

Testing:
We can run our entire test case by running the following command at command line

$ dropdb castagency
$ createdb castagency
$ psql castagency < db.psql
$ python test_app.py
```
