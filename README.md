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
- 400: Permissions were not included in the JWT.
- 400: Unable to parse authentication token.
- 400: Unable to parse authentication token.
- 400: Unable to find the appropriate key.

- 401: Authorization header is expected.
- 401: Authorization header must start with "Bearer".
- 401: Token not found.
- 401: Authorization header must be bearer token.
- 401: Authorization malformed.
- 401: Token expired.
- 401: Incorrect claims. Please, check the audience and issuer.

- 403: Permission denied.

- 404: Resource Not Found.

- 405: Method Not Allowed

- 422: Not Processable 

### Endpoints 

#### GET /

```
{
    "message": "Hello World",
    "success": true
}
```

#### GET /movies
- Fetches a paginated list of movies.
- Returns: list of movies ordered by id.
- Results are paginated in groups of 10.
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
    "success": true
}
```

#### GET '/actors'
- Fetches a paginated list of actors.
- Returns: list of actors ordered by id.
- Results are paginated in groups of 10.
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
    "success": true
}
```

#### POST '/movies'
- Create a new movie.
- Request Arguments: { title: String, release_date: DateTime }.
- Returns: An object with `success: True` and the new movie inside an array.
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
- Create a new actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the new actor inside an array.
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
- Update a movie.
- Request Arguments: { title: String, release_date: DateTime }.
- Returns: An object with `success: True` and the updated movie inside an array.
```
{
    "movie": [
        {
            "id": 4,
            "release_date": "Wed, 29 Jul 2020 21:12:59 GMT",
            "title": "Die Hard"
        }
    ],
    "success": true
}
```

#### Patch '/actors/<actor_id>'
- Update an actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the updated actor inside an array.
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
    "success": true
}
```

#### DELETE '/movies/<movie_id>'
- Removes a movie from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted movie
```
{
    "delete": 1,
    "success": true
}
```

#### DELETE '/actors/<actor_id>'
- Removes an actor from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted actor
```
{
    "delete": 1,
    "success": true
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
