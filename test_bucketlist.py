import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """ Bucketlist test case """

    def setUp(self):
        """ Define test variables and init app """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name':'Go to vacation'}

        # bind the app to current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketlist_create(self):
        """ Test API on creating a bucketlist (POST Request) """
        res = self.client().post('/bucketlist', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to vacation', str(res.data))

    def test_api_get_all_bucketlists(self):
        """ Test API to get all data in bucketlist (GET Request) """
        res = self.client().post('/bucketlist', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlist')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to vacation', str(res.data))

    def test_api_get_bucketlist_by_id(self):
        """ Test API to get bucketlist by id """
        res_post = self.client().post('/bucketlist', data=self.bucketlist)
        self.assertEqual(res_post.status_code, 201)
        res_in_json = json.loads(res_post.data.decode('UTF-8').replace("'", "\""))
        res = self.client().get(f"/bucketlist/{res_in_json['id']}")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to vacation', str(res.data))

    def test_api_get_bucketlist_by_id_not_exist(self):
        """ Test API to get bucketlist by id when id does not exist """
        res = self.client().get(f"/bucketlist/99")
        self.assertEqual(res.status_code, 404)

    def test_api_edit_bucketlist(self):
        """ Test API to edit bucketlist (PUT Request) """
        res_post = self.client().post('/bucketlist', data={'name': 'Wake up, Eat, Code, Sleep & Repeat'})
        self.assertEqual(res_post.status_code, 201)
        res_post_in_json = json.loads(res_post.data.decode('UTF-8').replace("'", "\""))
        id = res_post_in_json['id']
        res_put = self.client().put(
            f'bucketlist/{id}',
            data={
                'name': "Don't forget to exercise"
            }
        )
        self.assertEqual(res_put.status_code, 200)
        res = self.client().get(f'/bucketlist/{id}')
        self.assertIn("exercise", str(res.data))

    def test_api_delete_bucketlist(self):
        """ Test API to delete bucketlist (DELETE Request) """

        res_post = self.client().post('/bucketlist', data={'name': "Don't forget to exercise"})
        self.assertEqual(res_post.status_code, 201)
        res_post_in_json = json.loads(res_post.data.decode('UTF-8'))
        id = res_post_in_json['id']
        res_delete = self.client().delete(f"/bucketlist/{id}")
        self.assertEqual(res_delete.status_code, 200)

        # should return 404 after delete the data
        res = self.client().get(f'/bucketlist/{id}')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables after running a function of test."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

        # return super().tearDown()

# make this file executable
if __name__ == "__main__":
    unittest.main()


