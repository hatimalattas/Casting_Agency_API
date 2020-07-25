import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

# Set environment variables
os.environ['ASSISTANT_TOKEN'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNwMThwSXd0V1c2TGhpNFkybktBNiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MTQ1My51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxYzFiOTZiYmQ4Y2UwMDNkNjFlZjdkIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3ktYXBpIiwiaWF0IjoxNTk1NzEwOTk0LCJleHAiOjE1OTU3MTgxOTQsImF6cCI6IlcyR2E1QjBWNHREQTBlSzVNS0hBUng4aVdkNG16MDFsIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.eNOkAol_DHoo6kgLMRqcktA_1OAZ1Ld3dcjl0QtS9h76FcWfhhUGun73pBTBxtB0bKuS4boAbdS1VtN_4cM4sPxzsJdsNiU6XvZCbB5BPemeg72S4Yi_p1iW2kgCqngCsfMj1UidCwgmIdENrSm907PC_lkjwW1_4sRmC4YRaiXjLoXJ6BMp7qpJdEfN5op9l891UB6OsSOB2aA9NXLjCAG8_RPP_AkA6vd9XJA9FfWZX06yIyQhCB3a2CoeJpOOSI9Bz_7fuA5AZlmzBhRVph2ADalUDuKzCDcKc3hc0Uzb0Pa_nMmlXSIkH7D78hsz5okdClgkRiySoAPYd8RrHA'

os.environ['DIRECTOR_TOKEN'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNwMThwSXd0V1c2TGhpNFkybktBNiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MTQ1My51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxYzNjNTAzMTQ5OTkwMDNkMDRmMTAxIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3ktYXBpIiwiaWF0IjoxNTk1NzExMTk5LCJleHAiOjE1OTU3MTgzOTksImF6cCI6IlcyR2E1QjBWNHREQTBlSzVNS0hBUng4aVdkNG16MDFsIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.priMMqs06CS20HPHccAwF0lGR6nqNrDsSV3uezZJn2u5DQXvO3D3W2_82fq6-_WKGx7jV4BRHDMG-Pjsjqvm8R3oV2CyHXTlMzYl70BugvUnYeIa8nZNxGVX7PCl1LLh7xbozz30OYv7MJxG32TlNB7q10m8PYrSxKnPZGRqBgbOgODPsCcl3mRJjoNEuUDqvDJytoth-A-JC3JqPIgN4fyPSTrwQsigT5H2LCUvRCdtyJs1bmrCsmJ-JrIT93aKg8FHL5-KsB1u1I70EOrabRLvQjpqJkwTc4zXvxv4kthV4Jwj08Li5RinX5aeOiPOJOFNIeiyMcBxAbwGHcrdsQ'

os.environ['PRODUCER_TOKEN'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNwMThwSXd0V1c2TGhpNFkybktBNiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MTQ1My51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxYzEyNDgzMWExMjIwMDM3Zjk3NzYxIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3ktYXBpIiwiaWF0IjoxNTk1NzExNDI5LCJleHAiOjE1OTU3MTg2MjksImF6cCI6IlcyR2E1QjBWNHREQTBlSzVNS0hBUng4aVdkNG16MDFsIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.eQ0-7GNEN6SQc15EQNG-BnQPCQWNMU7lHzKqnZ2R80hJHW8mGGDELZBe9voBGHQBKFfOnMtxFtoDbGPtjojE-HSmCT-mZ-HzrttM8ykuncpQQyF4qqOvs4oarUql7YrssKloHY1fSCxzJoZeR-dwiC0R0WBrKNWFa9-2TUHPrVwIIKxG7KR_vTW3a6zJ0lt8pnY-0Qo5lBVR9me6dgcjaVlDhHHPTyrTWHROnPCU-Jkh0V6YS4wSP0NFcuLVfL3Br3fj_mjTvWpp39yjAguv-CLZHS7MWBNUb_UKytUIkW6IUHXMAyZBo-KNTedm78l1XOaEMk8K59aDR7a6jnPZxw'

# Get environment variables
assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
director_token = "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
producer_token = "Bearer {}".format(os.environ.get('PRODUCER_TOKEN'))

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            
            # create all tables
            self.db.create_all()

        self.new_actor = {
        'name': 'John Doe',
        'age': 20,
        'gender': 'Male'
        }

        self.new_actor_2 = {
        'name': 'Nate',
        'age': 20,
        'gender': 'Male'
        }

        self.update_actor = {
        'name': 'Claire',
        'age': 20,
        'gender': 'Female'
        }

        self.new_movie = {
        'title': 'Avengers 2',
        'release_date': '2021-10-1 04:22'
        }

        self.new_movie_2 = {
        'title': 'Avengers 4',
        'release_date': '2021-10-1 04:22'
        }

        self.update_movie = {
        'title': 'Toy Story 12',
        'release_date': '2021-10-1 04:22'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  ----------------------------------------------------------------
    #  Success behavior tests
    #  ----------------------------------------------------------------
    def test_get_movies(self):
        res = self.client().get('/movies', headers={ "Authorization": ( assistant_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors (self):
        res = self.client().get('/actors', headers={ "Authorization": ( assistant_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actors (self):
        res = self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( director_token ) })
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_create_movies (self):
        res = self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actors (self):
        self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
        res = self.client().patch('/actors/1', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_update_movies (self):
        self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( director_token ) })
        res = self.client().patch('/movies/1', json=self.update_movie, headers={ "Authorization": ( director_token ) })
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_actors (self):
        self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
        self.client().post('/actors', json=self.new_actor_2, headers={ "Authorization": ( producer_token ) })
        res = self.client().delete('/actors/2', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], 2)
        self.assertTrue(data['success'])

    def test_delete_movies (self):
        self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
        self.client().post('/movies', json=self.new_movie_2, headers={ "Authorization": ( producer_token ) })
        res = self.client().delete('/movies/2', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], 2)
        self.assertTrue(data['success'])

    #  ----------------------------------------------------------------
    #  Error behavior tests
    #  ----------------------------------------------------------------
    def test_401_get_actors (self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_get_movies (self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_401_create_actors (self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_create_movies (self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_update_actors (self):
        res = self.client().patch('/actors/1000', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_update_movies (self):
        res = self.client().patch('/movies/1000', json=self.update_movie, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_404_delete_actors (self):
        res = self.client().delete('/actors/1000', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_404_delete_movies (self):
        res = self.client().delete('/movies/1000', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
