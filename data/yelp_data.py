
import json
import requests

from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

CLIENT_ID = "g9OIa3eB5Hmh6MJ2lfBVLA"
CLIENT_SECRET = "LsTMxgHqlpBTSgha2PczFQ42DZkYS3rbnuVgJ2unb5aEwoVFfucuifnGzFcr0MPh"


def obtain_bearer_token():
    """Use this to request an access token from YELP API using client ID and Secret. 
    Access token 'POST' request line 43. Access token is returned in the "response.json"
    { "access_token": "ACCESS_TOKEN",
	  "token_type": "bearer",
	  "expires_in": 15552000
	}
	Called "bearer_token" after the response is received. 
    """

    url = 'https://api.yelp.com/oauth2/token'
    assert CLIENT_ID, "g9OIa3eB5Hmh6MJ2lfBVLA"
    assert CLIENT_SECRET, "LsTMxgHqlpBTSgha2PczFQ42DZkYS3rbnuVgJ2unb5aEwoVFfucuifnGzFcr0MPh"
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


# AFTER RUNNING ^^^ 
# SAVING TOKEN HERE!

token = 'CaO3oftZxwrxxm4-FTzcyOB5za_nfVcl4JvajMwqF-6dIX6SxbAZaPVZa_7WPuRbsdY0P6Fql0yQ405TdqSxpdaurgyX4cC-YnYMzd9IAh6d-Rr273HHi8Tnq2MTWXYx'




def request(url, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """

    url_params = url_params or {}
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()




# THIS WORKED TO OBTAIN 50 BIZ FROM SF

# 1. data = request('https://api.yelp.com/v3/businesses/search', token,url_params={'location': 'San Francisco'})
# 2. data.keys()    <--- got all big column names in huge data
# 3. data['businesses']  <---- showed all the data with in businesses table

# 1. data = request('https://api.yelp.com/v3/businesses/search', token,url_params={'location': 'San Francisco','limit':50, 'offset':0})
# 2. [biz['name'] for biz in data['businesses']]   <-- showed me 50 business names! in a list
# 3. [(biz['name'], biz['location'], biz['phone']) for biz in data['businesses'][:10]]   <-- shows me 3 columns of info for 10 businesses




# data = request('https://api.yelp.com/v3/businesses/search', token,url_params={
										#'location': 'San Francisco','limit':50, 'offset':0})
# the above is what I would use if I needed to request an additional 50 businesses in SF. 
# instead planning to do seperate requests for MTV, PA, Sunnyvale, Redwood City, Berkeley, Oakland, San Bruno, etc.




# sf_request = request('https://api.yelp.com/v3/businesses/search', token, url_params={'location': 'San Francisco'})
# seed_file = open('seed_data.txt', 'w')
# for business in sf_request['businesses']:
# 	display_address = ", ".join(business['location']['display_address'])

# 	seed_file.write(business['name'] + "|" + display_address + "|" + business['phone']+ "\n") 

	




seed_file = open('seed_data.txt', 'w')
cities = ['San Francisco', 'Palo Alto', 'Mountain View', 'Sunnyvale', 'Millbrae', 
          'Burlingame', 'San Mateo', 'Belmont', 'Menlo Park', 'San Jose', 'Oakland', 
          'Berkeley', 'San Leandro', 'Hayward', 'Santa Clara', 'Milpitas', 'Daly City',
          'East Palo Alto', 'Los Altos', 'South San Francisco'] 
for city in cities:
    sf_request = request('https://api.yelp.com/v3/businesses/search', 
                          token, url_params={'location': city,'limit':50})
    # import pdb; pdb.set_trace()
    for business in sf_request['businesses']:
        display_address = ", ".join(business['location']['display_address'])
        lat = str(business['coordinates']['latitude'])
        lng = str(business['coordinates']['longitude'])
        line = business['name'] + "|" + display_address + "|" + business['url'] + "|" + business['phone']+ "|" + lat + "|" + lng + "\n"
        seed_file.write(line.encode('utf8')) 


# do less seed_data.txt  to view in command file


seed_file.close()





#For number data:
for i in range(1001):
    print (random.randrange(250,1500,2)), (random.randrange(5,20,3)), (random.randrange(10,40,3))





