"""Models and database functions for OOH_listings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """Users registered on the website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_photo=db.Column(db.String(1000)) #url profile pics
    ad_image = db.Column(db.String(1000)) 
    description = db.Column(db.Text)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s name=%s lastname=%s \
                email=%s>" % (self.user_id, 
                              self.first_name, 
                              self.last_name,  
                              self.email)




class Listings(db.Model):
    """Listings on the website."""

    __tablename__ = "listings"

    listing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    business = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    zipcode = db.Column(db.String(64), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    height_max = db.Column(db.Integer)
    width_max = db.Column(db.Integer)
    price= db.Column(db.Integer)
    owner_picture = db.Column(db.String(1000))
    listing_photo = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    
    # Define relationship to owner
    owner = db.relationship("User", backref="listings")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Listing ID: %s Address: %s Phone: %s \
                Address: %s>" % (self.listing_id,
                                 self.address, 
                                 self.phone)





class Rental_Records(db.Model):
    """Record of all rentals made between Owners and Advertisers on the website."""

    __tablename__ = "rentals"

    rental_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'))
    advertiser_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean, default=False) #function?
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    total_price = db.Column(db.Integer)
    image = db.Column(db.String(200))
    
    # Define relationship to owner, advertiser, and listing
    listing = db.relationship("Listings", backref="rentals")
    advertiser = db.relationship("User", backref="rentals")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Listing ID: %s Active: %s Start Date: %s \
                End Date: %s Price: %s>" % (self.listing_id,
                                       self.in_active,
                                       self.start_date,
                                       self.end_date,
                                       self.price)





##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///OOH_listings'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."