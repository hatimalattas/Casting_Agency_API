# Casting Agency API

The Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies.
This api is responsible for checking permissions and handling CRUD for an Actor and Movie models

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Role-based access control (RBAC)
In computer systems security, role-based access control or role-based security is an approach to restricting system access to authorized users.

In this project we have 3 types of users:
#### Casting Assistant
- Can view actors and movies

#### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

#### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "error": 405,
  "message": "method not allowed",
  "success": false
}
```
The API will return the following errors when requests fail:
- 400: Bad Request
- 401: Anauthorized
- 403: Forbidden
- 404: Resource Not Found
- 409: Duplicate Resource
- 422: Not Processable 
- 500: Server Error

### Endpoints 

#### GET /

```
{
    "message": "Hello World",
    "success": true
}
```

#### GET /movies
Returns a paginated list of movies, a success value, and total number of movies
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/movies.

Sample response output:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Wed, 29 Jul 2020 21:06:33 GMT",
            "title": "Inception"
        },
        {
            "id": 2,
            "release_date": "Wed, 29 Jul 2020 21:06:50 GMT",
            "title": "The Dark Knight"
        },
        {
            "id": 3,
            "release_date": "Wed, 29 Jul 2020 21:07:14 GMT",
            "title": "Joker"
        }
    ],
    "success": true,
    "total_movies": 3
}
```

#### GET '/actors'
Returns a paginated list of actors, a success value, and total number of actors
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/actors.

Sample response output:
```
{
    "actors": [
        {
            "age": 23,
            "gender": "Male",
            "id": 1,
            "name": "John"
        },
        {
            "age": 40,
            "gender": "Male",
            "id": 2,
            "name": "Mark"
        },
        {
            "age": 33,
            "gender": "Female",
            "id": 3,
            "name": "Jenny"
        }
    ],
    "success": true,
    "total_actors": 3
}
```

#### POST '/movies'
Returns a list of the movie that was posted, the id of the movie that was posted, a success value, and total number of movies
Sample curl: 
curl http://localhost:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Printer", "release_date": "Wed, 29 Jul 2020 21:30:42 GMT"}'.

Sample response output:
```
{
    "created": 5,
    "movies": [
        {
            "id": 5,
            "release_date": "Wed, 29 Jul 2020 21:30:42 GMT",
            "title": "Die Hard 2"
        }
    ],
    "success": true,
    "total_movies": 5
}
```

#### POST '/actors'
Returns a list of the actor that was posted, the id of the actor that was posted, a success value, and total number of actors
Sample curl: 
curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Mark", "gender": "Male", "age":29}'.

Sample response output:
```
{
    "actors": [
        {
            "age": 29,
            "gender": "Male",
            "id": 10,
            "name": "Mark"
        }
    ],
    "created": 10,
    "success": true,
    "total_actors": 5
}
```


#### Patch '/movies/<movie_id>'
Returns a list of the updated movie, a success value, and total number of movies.
Sample curl:
curl http://localhost:5000/movies/4 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Die Hard"}'.

Sample response output:
```
{
    "movie": [
        {
            "id": 4,
            "release_date": "Wed, 29 Jul 2020 21:12:59 GMT",
            "title": "Die Hard"
        }
    ],
    "success": true,
    "total_movies": 5
}
```

#### Patch '/actors/<actor_id>'
Returns a list of the updated actor, a success value, and total number of actors.
Sample curl:
curl http://localhost:5000/actors/4 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Jimmy"}'.

Sample response output:
```
{
    "actor": [
        {
            "age": 29,
            "gender": "Male",
            "id": 4,
            "name": "Jimmy"
        }
    ],
    "success": true,
    "total_actors": 4
}
```

#### DELETE '/movies/<movie_id>'
Returns the id of the deleted movie, a success value, and total number of movies.
curl http://localhost:5000/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}".

Sample response output:
```
{
    "delete": 1,
    "success": true,
    "total_movies": 3
}
```

#### DELETE '/actors/<actor_id>'
Returns the id of the deleted actor, a success value, and total number of actors.
curl http://localhost:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}".

Sample response output:
```
{
    "delete": 1,
    "success": true,
    "total_actors": 3
}
```

## Testing
#### Running tests locally
To run the tests from ./test_app.py, first make sure you have ran and executed the setup.sh file to set the enviorment.

After setting the enviorment start your local postgress server:
```bash
pg_ctl -D /usr/local/var/postgres start
```

Then run the follwing commands to run the tests:
```
dropdb casting_agency
createdb casting_agency
python test_app.py
```
## Deployment
This project is hosted at https://casting-agency1453.herokuapp.com/


## Authors
Yours truly, Hatim Alattas
