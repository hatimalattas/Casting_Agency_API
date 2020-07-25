import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth
from models import setup_db, db, Movie, Actor

DEFAULT_LIMIT = 10


def paginate_response(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DEFAULT_LIMIT
    end = start + DEFAULT_LIMIT

    formatted_selection = [item.format() for item in selection]
    paginated_selection = formatted_selection[start:end]

    return paginated_selection

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    Migrate(app, db)

    # set up CORS, allowing all origins
    CORS(app, resources={'/': {'origins': '*'}})
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE')
        return response

    #  ----------------------------------------------------------------
    #  TEST
    #  ----------------------------------------------------------------
    @app.route("/")
    def hello():
        
        return jsonify({
            'success': True,
            'message': 'Hello World'
        })
    #  ----------------------------------------------------------------
    #  GET Movies
    #  ----------------------------------------------------------------
    @app.route("/movies")
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_response(request, selection)
        
        return jsonify({
            'success': True,
            'movies': current_movies
        })

    #  ----------------------------------------------------------------
    #  GET Actors
    #  ----------------------------------------------------------------
    @app.route("/actors")
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_response(request, selection)

        return jsonify({
            'success': True,
            'actors': current_actors
        })

    #  ----------------------------------------------------------------
    #  POST Movies
    #  ----------------------------------------------------------------
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        movie = Movie(title=new_title,
                      release_date=new_release_date)
        movie.insert()

        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_response(request, selection)

        return jsonify({
            'success': True,
            'created': movie.id,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })

    #  ----------------------------------------------------------------
    #  POST Actors
    #  ----------------------------------------------------------------
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        actor = Actor(name=new_name,
                      age=new_age,
                      gender=new_gender)
        actor.insert()

        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_response(request, selection)

        return jsonify({
            'success': True,
            'created': actor.id,
            'actors': current_actors,
            'total_actors': len(Actor.query.all())
        })
    #  ----------------------------------------------------------------
    #  PATCH Movies
    #  ----------------------------------------------------------------
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        # get drink by id
        movie = Movie.query.get(movie_id)

        # Abort 404 if the movie was not found
        if movie is None:
            abort(404)

        # get request body
        body = request.get_json()

        # update title if present in body
        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']

        # Update the movie with the requested fields
        movie.update()

        # Return the updated movie
        return jsonify({
            'success': True,
            'movies': [Movie.query.get(movie_id).format()]
        })

    #  ----------------------------------------------------------------
    #  PATCH ACTORS
    #  ----------------------------------------------------------------
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        # get drink by id
        actor = Actor.query.get(actor_id)

        # Abort 404 if the movie was not found
        if actor is None:
            abort(404)

        # get request body
        body = request.get_json()

        # update title if present in body
        if 'name' in body:
            actor.name = body['name']
        if 'age' in body:
            actor.age = body['age']
        if 'gender' in body:
            actor.gender = body['gender']

        # Update the movie with the requested fields
        actor.update()

        # Return the updated movie
        return jsonify({
            'success': True,
            'actors': [Actor.query.get(actor_id).format()]
        })

    #  ----------------------------------------------------------------
    #  DELETE MOVIES
    #  ----------------------------------------------------------------
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        # get movie by id
        movie = Movie.query.filter_by(id=id).one_or_none()

        # if movie not found
        if movie is None:
            abort(404)

        try:
            # delete movie from database
            movie.delete()
        except:
            # server error
            abort(500)

        # return status and deleted movie id
        return jsonify({
            'success': True,
            'delete': id
        })

    #  ----------------------------------------------------------------
    #  DELETE ACTORS
    #  ----------------------------------------------------------------
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        # get actor by id
        actor = Actor.query.filter_by(id=id).one_or_none()

        # if actor not found
        if actor is None:
            abort(404)

        try:
            # delete actor from database
            actor.delete()
        except:
            # server error
            abort(500)

        # return status and deleted actor id
        return jsonify({
            'success': True,
            'delete': id
        })

        
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)
 