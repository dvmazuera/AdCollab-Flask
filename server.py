from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model_project import connect_to_db, db, User, Listings, Rental_Records

import sendgrid
import os
from sendgrid.helpers.mail import *

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
import json
import bcrypt
import re

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

#____________________________________________________________________________________________



@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


# Link here from HOMEPAGE just for me to see all users --- REMOVE FOR FINAL !
@app.route("/view_users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


#LISTING LIST
# Link here from HOMEPAGE just for me to see all listings --- REMOVE FOR FINAL !
@app.route("/view_listing")
def listings_list():
    """Show list of listings."""

    listings = Listings.query.order_by('listing_id').all()
    return render_template("listings_list.html",
                            listings=listings)


##########################################################################################################

#LOGIN 

@app.route('/login', methods=["POST"])
def login_form():
    """ Login form. """
    return render_template("homepage.html")



@app.route('/process_login', methods=["POST"])
def process_login():
    """  Process entries in login form. """

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()



    if not user:
        flash("Email not found. Please register")
        return redirect("/")
    else:
        if password == user.password:
            password = password.encode('utf8')
            hashedpass = user.password.encode('utf8') 
            session["user"] = user.user_id
            flash("Thank you for logging In")
            return redirect("/entry_page")

        elif password != user.password:
             flash("Incorrect password Try again")
             return redirect("/")



@app.route('/logout')
def logout():
    """Log out."""

    del session["user"]
    flash("Logged Out.")
    return redirect("/")



############################################################################################################

# ADD A SPLIT PANE 

@app.route('/entry_page')
def entry_page():
    """     """

    return render_template("entry_page.html")



#NEW USER

@app.route('/new_user')
def new_user():
    """Create a user page."""

    return render_template("add_user.html")




@app.route('/process_new_user', methods=['POST'])
def process_new_user():
    """Process new user."""

    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    email = request.form.get("email")
    email = email.lower()
    password = request.form.get("password")
    password = password.encode('utf8') 
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    phone = request.form["phone"]
    phone = re.sub(r"[\-\(\)\.\s]+", "", phone)
    zipcode = request.form.get("zipcode")
    description = request.form.get("description")


    if db.session.query(User).filter(User.email==email).first():
        flash('This email belongs to an existing account. Please login.')
        return redirect('/new_user')
    else:
        if len(email) > 25:
            flash('Email contains too many characters. Please try again')
            return redirect('/new_user')
        if len(phone) != 10:
            flash("Invalid number. Make sure to include area code.")
            return redirect('/new_user')
        else:    
            user = User(first_name=first_name, last_name=last_name, phone=phone, 
                        email=email, password=hashed)
            db.session.add(user)
            db.session.commit()
           
            flash("User added successfully!!!")
            session["user"] = user.user_id

            return redirect("/entry_page")




@app.route('/account_info')
def display_user_information():
    """displays user information"""

    if "user" in session:
        user = User.query.get(session["user"])
        user_photo = "/static/img/" + str(user.user_photo)
        user_ad = "/static/img/" + str(user.ad_image)
        user_id = user.user_id

        listing = Listings.query.filter(Listings.owner_id==user_id).first()
        print listing


        return render_template('account_info.html', user=user,
                                                    user_photo=user_photo,
                                                    user_ad=user_ad)
    else:
        flash("Please login in to view")
        return redirect ('/')



@app.route('/update_account', methods=["POST"])
def update_account_info():
    """Updates account information"""

    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")
    description = request.form.get("description")
    user = User.query.get(session["user"])

    if email:
        if len(email) > 25:
            flash('Password or email too long')
        else:
            email = email.lower()
            user.email = email.rstrip()
            password = password.rstrip()
            password = password.encode('utf8') 
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = hashed
            flash('Information Updated')
    
    if phone:
        phone=re.sub(r"[\-\(\)\.\s]+", "", phone)
        if len(phone) != 10:
            flash("Invalid number. Make sure to include area code.")
        else:
            user.phone = phone.rstrip()
            flash('Information Updated')
        
    
    db.session.add(user)
    db.session.commit()

    return redirect('/account_info')







###################################################################################################

#NEW LISTING
 
@app.route('/new_listing')
def new_listing():
    """Create a listing page."""

    return render_template("add_listing.html")



@app.route('/process_new_listing', methods=['POST'])
def process_new_listing():
    """Process new listing to Listings DB."""

    # Get form variables
    business = request.form.get("business")
    phone = request.form.get("phone")
    phone = re.sub(r"[\-\(\)\.\s]+", "", phone)
    address = request.form.get("address")
    zipcode = request.form.get("zipcode")
    height_max = request.form.get("height")
    width_max = request.form.get("width")
    price = request.form.get("price")
    description = request.form["description"]

  
    listing = Listings(business=business, phone=phone, address=address, zipcode=zipcode, 
                       height_max=height_max, width_max=width_max)

    db.session.add(listing)
    db.session.commit()

    flash("Listing added successfully!!!")

    return redirect("/")




@app.route('/listings.json')
def listing_info():
    """JSON information about listings to be passed to Google MAP API."""

    listings = {
        listing.listing_id: {
            "ownerId": listing.owner_id,
            "business": listing.business,
            "phone": listing.phone,
            "address": listing.address,
            "zipcode": listing.zipcode,
            "Lat": listing.lat,
            "Long": listing.lng,
            "heightmax": listing.height_max,
            "widthmax": listing.width_max,
            "owner_picture": listing.owner_picture,
            "price": listing.price, 
            "listing_photo":listing.listing_photo,
            "description":listing.description
        }
        for listing in Listings.query.all()}

    return jsonify(listings)





@app.route("/listing/<int:listing_id>", methods=['GET'])
def listing_detail(listing_id):
    """Show info about listing. (copied from Ratings -- info about movie**)
    If a user is logged in, let them add/edit a rating.
    """
    user_id = session.get("user")
    print user_id
    user = User.query.filter_by(user_id=user_id).first()

    user_photo = "/static/img/" + str(user.user_photo)

    listing = Listings.query.get(int(listing_id))
    listing_owner_photo = "/static/img/" + str(listing.owner_picture)

    listing_image= "/static/img/" + str(listing.listing_photo)
  


    # raise Exception
    return render_template("listing_details.html", listing=listing,
                                                   user=user, 
                                                   listing_owner_photo=listing_owner_photo,
                                                   listing_image=listing_image,
                                                   user_photo=user_photo)





#######################################################################################################

# GOOGLE MAP's API page

@app.route('/advertise')
def advertise():
    """Create a listing page."""

    return render_template("map_select_listing.html")







@app.route('/search_zipcode')
def search_zipcode():
    """Show map of SF with search functionality on page."""


    zipcode = request.args.get("zipcode")

    return render_template("map_select_listing.html",
                            zipcode= zipcode)





@app.route('/filter_search.json')
def filter_search():
    """Show map of SF with filters."""

    low_price = int(request.args.get('lowPrice'))
    high_price = int(request.args.get('highPrice'))
    height = float(request.args.get('height'))
    width = float(request.args.get('width'))
    
    # Retrieves listings from db_queries
    listings = find_all_listings( height, width, low_price, high_price)

    return jsonify(listings)




def find_all_listings(height, width, low_price, high_price):
    """JSON information about FILTERED listings to be passed to Google MAP API."""

    listings = {
        listing.listing_id: {
            "ownerId": listing.owner_id,
            "business": listing.business,
            "phone": listing.phone,
            "address": listing.address,
            "zipcode": listing.zipcode,
            "Lat": listing.lat,
            "Long": listing.lng,
            "heightmax": listing.height_max,
            "widthmax": listing.width_max,
            "image": listing.listing_photo,
            "price": listing.price
        }
        for listing in Listings.query.filter( (Listings.height_max >= height), 
                                                 (Listings.width_max >= width), 
                                                 (Listings.price >= low_price), 
                                                 (Listings.price <= high_price)).all()}
    return listings




#######################################################################################################

@app.route('/emailDetail.json' , methods=['POST'])
def email_detail():
    """Show map of SF with filters."""

    rent_price = int(request.form.get('rent_price'))
    start_month = request.form.get('startMonth')
    end_month = request.form.get('endMonth')
    ad_height = float(request.form.get('adHeight'))
    ad_width = float(request.form.get('adWidth'))
    requester_name = request.form.get('requesterName')
    requester_phone = request.form.get('requesterPhone')
    requester_email = request.form.get('requesterEmail')
    requester_comment = request.form.get('requesterComment')
    listing_email = request.form.get('listingEmail')
    listing_name = request.form.get('listingName')
    listing_business = request.form.get('listingBusiness')

    # Retrieves listings from db_queries
    email = request_email(rent_price, start_month, end_month,ad_height, ad_width, requester_name, requester_phone, requester_email, requester_comment, listing_name, listing_email, listing_business)
    # confirm = confirm_request_email(rent_price, start_month, end_month,ad_height, ad_width, requester_name, requester_phone, requester_email, requester_comment, listing_name, listing_email, listing_business)
    
    # record = Rental_Records(listing_id=listing_business, rental_id=requester_name, start_date=start_month, end_date=end_month, total_price=rent_price)
    # requester_name, requester_phone, requester_email, requester_comment, listing_name, listing_email, listing_business

    # db.session.add(record) 
    # db.session.commit()


    return jsonify(email)



def request_email(rent_price, start_month, end_month,ad_height, ad_width, requester_name, requester_phone, requester_email, requester_comment, listing_name, listing_email, listing_business):
    print listing_email
    print listing_business

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("dvmazuera@gmail.com")
    to_email = Email("dvmcoupons@gmail.com")
    subject = "Your Listing:'" + listing_business + "' has Received a Request!"
    # content = Content("text/html", "<p> Hello " +listing_name + "! </p><br><p>"+ requester_name + " has shown interest in your listing! He would like to rent " + ad_height + "ft by " + ad_width + "ft of your available listing space for the months: " + start_month + " through " + end_month + " for a grand total of: $" + rent_price + ".</p><br><br><p>Here is a short comment from him: "+ requester_comment +" </p> CLICK <a href=\"" + link + "\">here</a> to see the info on your listing page and CONFIRM or DECLINE this request.</p><br><br><p>-AdCollab Marketing Team</p>")
    content = Content("text/html", "Hello ")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)




#     sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("dvmazuera@gmail.com")
#     to_email = Email("dvmcoupons@gmail.com")
#     subject = "Sending with SendGrid is Fun"
#     content = Content("text/plain", "and easy to do anywhere, even with Python")
#     mail = Mail(from_email, subject, to_email, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)






# def confirm_request_email(rent_price, start_month, end_month,ad_height, ad_width, requester_name, requester_phone, requester_email, requester_comment, listing_name, listing_email, listing_business):
#     sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("request@adcollab.com")
#     to_email = Email("dvmcoupons@gmail.com")
#     subject = "Your request has been sent for'" + listing_business + "'! - AdCollab"
#     # content = Content("text/html", "<p> Hello " +requester_name + "! </p><br><p> This email is to confirm that"+ listing_name + "from"+ listing_business+" has received your request email!</p><br><p> The email shows the following: </p><br><p>'"+ requester_name + "would like to rent " + ad_height + "ft by " + ad_width + "ft of the available listing space for the months: " + start_month + " through " + end_month + " for a grand total of: $" + rent_price + ".</p><br><br><p>Here is a short comment from him: "+ requester_comment +" </p> Once she has CONFIRMED or DECLINED this request, we will notify you through email. </p><br><br><p>-AdCollab Marketing Team</p>")
#     content = Content("text/html", "Hello ")
#     mail = Mail(from_email, subject, to_email, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)





# @app.route('/submit-request/<listing_id>.json', methods=['POST'])
# def submit_request(listing_id):
#     """make trie viewable by another user"""

#     share_email = request.form.get("email")
#     total_price = request.args.get('rent-price')
#     start_date = request.args.get('startMonth')
#     end_date = request.args.get('endMonth')
#     ad_height = float(request.args.get('adHeight'))
#     ad_width = float(request.args.get('adWidth'))
#     requester_id = session['user']
#     listing_business = Listing.query.get(listing_id).business

#     requester_name = request.args.get('userName')
#     user_comment = request.args.get('userComment')   
#     listing_link = 'http://localhost:5000/listing/' + listing_id


#     owner = User.query.filter_by(email=share_email).all()
#     owner_id= owner.id
#     record = Rental_Records(listing_id=listing_id, requester_id=requester_id, owner_id=owner_id, start_date=start_date, end_date=end_date, 
#                 ad_height=ad_height, ad_width=ad_width, total_price=total_price, is_active=is_active)

#     db.session.add(record) 
#     db.session.commit()

#     request_email(share_email, listing_business, requester_name, total_price, start_date, end_date, ad_height, ad_width, user_comment, listing_link)
    
#     flash("Booking Request Emailed!!!")

#     return redirect("/book_listing")

  







@app.route("/book_listing")
def book_listings():
    """Show list of listings."""

    rentals = Rental_Records.query.order_by('rental_id').all()

    return render_template("use_rental_confirmation.html",
                            rentals=rentals)





#_______________________________________________________________________________________________

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
