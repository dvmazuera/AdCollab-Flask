
import server
import unittest
from model_project import connect_to_db, db, User, Listings
from seed import load_users, load_listings, load_numbers
from flask import json



class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        connect_to_db(server.app, 'postgresql:///testdb')
        db.create_all()
        load_users()
        load_listings()
        load_numbers()

    def tearDown(self):
        # We don't need to do anything here; we could just
        # not define this method at all, but we have a stub
        # here as an example.
        print "(tearDown ran)"
        db.session.close()
        db.drop_all()


    # Test extracting correct data

    def test_user_data(self):
        result = self.client.get('/view_users')
        user = User.query.get(1)

        self.assertEquals(user.first_name, 'Cathrine')

    def test_listing_data(self):
        result = self.client.get('/view_listings')
        listing = Listings.query.get(1)

        self.assertEquals(listing.business, 'The Temporarium Coffee & Tea')




    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')

        self.assertIn('<button onclick="window.location.href=\'/new_user\'">Create An Account</button>', result.data)


    # Testing Correct Login, Incorrect login, Incorrect password.

    def test_process_login1(self):
        result = self.client.post('/process_login', data={'email':'cgrabban0@va.gov',
                                                         'password' : 'DOwLzwtLHz7j'},follow_redirects=True)

        self.assertIn('<button onclick="window.location.href=\'/logout\'">Logout</button>', result.data)



    def test_process_login2(self):
        result = self.client.post('/process_login', data={'email':'gnyt@a.com',
                                                         'password' : 'DOwLzwtLHz7j'}, follow_redirects=True)

        self.assertIn('<button onclick="window.location.href=\'/new_user\'">Create An Account</button>', result.data)



    def test_process_login3(self):
        result = self.client.post('/process_login', data={'email':'cgrabban0@va.gov',
                                                         'password' : 'DOwLzwtnhfnrhtez7j'}, follow_redirects=True)

        self.assertIn('<button onclick="window.location.href=\'/new_user\'">Create An Account</button>', result.data)



    # Test listing filters request to map API

    def test_filter_search(self):
        # import pdb; pdb.set_trace()
        # result = self.client.get('/filter_search.json', data={'lowPrice':'100','highPrice':'300','height':'11','width':'9'})
        result = self.client.get('/filter_search.json?lowPrice=100&highPrice=300&height=11&width=9')
        expected_keys = [u'742', u'748', u'337', u'196', u'608', u'660', u'135', u'798', u'836', u'42', u'41', u'762', u'2', u'547', u'184', u'362', u'586', u'309', u'677', u'617', u'98', u'383', u'266', u'921', u'78', u'907', u'14', u'849', u'866', u'643', u'808', u'722', u'352', u'510', u'435', u'517']

        data = json.loads(result.data)
        self.assertEquals(data.keys(),expected_keys)









#______________________________________________________________________________________________

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
