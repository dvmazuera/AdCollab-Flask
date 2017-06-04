"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func

from model_project import User, Listings, Rental_Records, connect_to_db, db
from server import app



def load_users():
    """Load users from u.user into database."""

    print "Users"
    for i, row in enumerate(open("user_data.csv")):
        row = row.rstrip()
        user_photo, username, first_name, last_name, email, password, phone, ad_image, state, description= row.split(",")

        user = User(first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    password=password,
                    description=description, 
                    user_photo=user_photo,
                    ad_image=ad_image)
        
        db.session.add(user)
        if i % 100 == 0:
            print i
    db.session.commit()



def load_listings():
    """Load movies from u.item into database."""

    print "Listings"
    for i, row in enumerate(open("seed_data.txt")):
        row = row.rstrip()

        try:
            business, address, owner_picture, phone, lat, lng, user_id, listing_photo = row.split("|")
        except ValueError:
            import pdb; pdb.set_trace()

        zipcode = address[-5:]   
        lat = lat[:-3]
        #this is making a new Listing ROW!
        listings = Listings(business=business,
                      address=address,
                      zipcode=zipcode,
                      phone=phone,
                      lat=float(lat),
                      lng=float(lng),
                      owner_picture=owner_picture,
                      listing_photo=listing_photo)

        db.session.add(listings)
        if i % 100 == 0:
            print i
    db.session.commit()



def load_numbers():
    """Load movies from u.item into database."""

    print "Listings"
    for i, row in enumerate(open("number_data.txt")):
        row = row.rstrip()
        #need to find the already made seeded table for listings and choose to fill in the "null" columns in THAT table
        listing = Listings.query.filter_by(listing_id=(i+1)).one()

        try:
            price, height, width = row.split(" ")
        except ValueError:
            import pdb; pdb.set_trace()

        #I dont need to make a new Listing row... instead sqlal is lettingme treatthe row already  as a object
        listing.price = price
        listing.height_max = height
        listing.width_max = width
        
        if i % 100 == 0:
            print i
    db.session.commit() #I dont need to add.. since I am not creating a new row.. just updating :)



def load_numbers():
    """Load movies from u.item into database."""

    # print "Listings"
    for i, row in enumerate(open("number_data.txt")):
        row = row.rstrip()
        #need to find the already made seeded table for listings and choose to fill in the "null" columns in THAT table
        listing = Listings.query.filter_by(listing_id=(i+1)).one()

        try:
            price, height, width = row.split(" ")
        except ValueError:
            import pdb; pdb.set_trace()

        #I dont need to make a new Listing row... instead sqlal is lettingme treatthe row already  as a object
        listing.price = price
        listing.height_max = height
        listing.width_max = width
        
        # if i % 100 == 0:
        #     print i
    db.session.commit() #I dont need to add.. since I am not creating a new row.. just updating :)






def set_val_Listing_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Listings.listing_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('listings_listing_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

#_________________________________________________

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_listings()
    load_numbers()

    # set_val_user_id()

 
