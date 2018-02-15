# AdCollab - Flask App


AdCollab is the Airbnb for outdoor ad space – enabling building owners to post available exterior wall space and connect with local businesses looking to advertise at affordable prices.

Users are able to search for listings in their area by zipcode, with the option to filter further by price and ad dimensions to find the perfect outdoor advertising space in their area. Best of all, users get to preview how their uploaded ads will appear on the listing’s ad space prior to making a selection! 

AdCollab helps the community two-fold: 1) ads help bring small businesses more foot traffic and 2) the profits from local ad rentals can help business owners in underrepresented communities keep their businesses up and help stall the steady trend towards gentrification.

[Click Below for YouTube DEMO][![AdCollab - Flask App](http://bit.ly/2GFAOcw)](https://youtu.be/Kn7PAk4YUso "AdCollab - Flask App")




 # Contents
* [Features](#features)
* [Installing](#installing)
* [Built with](#builtwith)
* [Coming Up](#comingup)


## <a name="features"></a>Features


##### User login/register page

![Landing Page](http://bit.ly/2DUf5jj)

##### User Profile - 
Profile for user to include contact info and identify as either an Advertiser or a Listing Owner.  
Option for user to *Upload Images* of their ads. (option later to preview uploaded ads on an image of the listing)

![User Profile](http://bit.ly/2DSb7DX)

##### Two Tracks - 
1) Advertiser? Search for available listings to advertise   - or  -  2) Building Owner? Create a new ad listing 

![Choose a Track](http://bit.ly/2BNYfN6)



##### Search for Listings -
Users filter for listings in their area by zipcode, with the option to filter further by price and ad dimensions. 

Google Maps API - Yelp API

![Search Map]( http://bit.ly/2FEA467 )


##### Preview Your Ad -
If user uploads ads to profile, a drag n' drop feature lets them preview how the ad will appear on the selected listing. 

![Drag n Drop](http://bit.ly/2E3Gn6r)


##### Contact the Owner -
Once selected, the cost to rent the ad space is calculated and all info is sent to the listing owner by email

SENDGRID API

![Send Info](http://bit.ly/2GFPxV2)




## <a name="installing"></a>Installing

Install PostgreSQL (Mac OSX)


Clone this repo:

```
https://github.com/dvmazuera/AdCollab-Flask.git
```

Create virtual environment on your laptop, inside a directory:

```
virtualenv env
source env/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```


Set up your database and seed images/content:

```
python model.py
python seed.py
```

Start running your server:

```
python server.py
```

Open up your browser and navigate to:

```
 'localhost:5000/'
```





## <a name="builtwith"></a>Built With                   


##### Backend

[Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), [PostgreSQL](https://www.postgresql.org/)

##### Frontend

JavaScript, HTML, CSS, [jQuery](https://jquery.com/), AJAX, [Jinja2](http://jinja.pocoo.org/docs/dev/)

##### APIs

[Google Maps API](https://developers.google.com/maps/), [Yelp API](https://api.yelp.com/v3/businesses/search/), [SendGrid API](https://www.sendgrid.com/API)


## <a name="comingup"></a>Version 2.0 Coming Up 

- **Password hashing:** Passwords will be hashed before being saved in DB
- **Email:** Complete sendgrid functionality
- **Listings:** Add additional features for listing owners.
- **Payments:** Process the full transaction from the site. 
