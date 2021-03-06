#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    # genres = db.Column(db.String(125)) This seems wrong since it sends all of them truncated
    genres = db.Column(db.ARRAY(db.String))
    address = db.Column(db.String(123))
    city = db.Column(db.String(121))
    state = db.Column(db.String(122))
    phone = db.Column(db.String(124))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(126))
    seeking_talent = db.Column(db.Boolean)
    seeking_description =  db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # genres = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description =  db.Column(db.String(500))
    image_link = db.Column(db.String(500))

    shows = db.relationship('Show', backref='Artist', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # id,name,genres,city,state,phone,website,facebook_link,seeking_venue,seeking_description,image_link
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  # Used mentor Satyajeet's pseudocode
  db_list = []
  db_dict = {}
  cities = Venue.query.distinct(Venue.city, Venue.state).all()
  for city in cities:
    #print("city", city)
    #print("city.city", city.city)
    #print("city type", type(city))
    #print("city.city type", type(city.city))
    db_dict['city'] = city.city
    db_dict['state'] = city.state
    venues = Venue.query.filter_by(city=city.city, state=city.state)
    ven_list = []
    for venue in venues:
      ven_dict = {}
      ven_dict['id'] = venue.id
      ven_dict['name'] = venue.name
      show_count = 0
      for show in venue.query.join('shows'):
        show_count+=1
      ven_dict['num_upcoming_shows']=show_count
      ven_list.append(ven_dict.copy())
    db_dict['venues'] = ven_list
    db_list.append(db_dict.copy()) # the pointer like behavior cost many hours!
  #print("json", db_list)
  db_json = json.dumps(db_list) # this totally destroyed the output by making it double quotes which is standard json
  #print('original', data)
  #print('json', db_json)
  data=db_list
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  #stmt = select([sometable]).where(sometable.c.column.ilike("%foobar%"))
  search_term = request.form.get('search_term', '')
  print(search_term)
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  print(venues)
  resp_dict = {}
  ven_count = 0
  ven_list = []
  for venue in venues:
    ven_count +=1
    ven_dict = {}
    ven_dict['id'] = venue.id
    ven_dict['name'] = venue.name
    show_count = 0
    for show in venue.query.join('shows'):
      show_count+=1
    ven_dict['num_upcoming_shows']=show_count
    ven_list.append(ven_dict.copy())
  resp_dict["count"] = ven_count
  resp_dict["data"] = ven_list

  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=resp_dict, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  venue = Venue.query.get(venue_id)
  ven_dict = {}
  ven_dict['id']=venue.id
  ven_dict['name']=venue.name
  ven_dict['genres']=venue.genres
  ven_dict['address']=venue.address
  ven_dict['city']=venue.city
  ven_dict['state']=venue.state
  ven_dict['phone']=venue.phone
  ven_dict['website']=venue.website
  ven_dict['facebook_link']=venue.facebook_link
  ven_dict['seeking_talent']=venue.seeking_talent
  ven_dict['image_link']=venue.image_link
  past_shows_list=[]
  upcoming_shows_list=[]
  past_shows_count = 0
  upcoming_shows_count = 0
  for show in Show.query.filter_by(venue_id=venue_id): # using the venue_id passed to function, not venue.id extracted above
    show_dict = {}
    #print('these shows', show.id, show.start_time)
    #print('now it is:', datetime.datetime.now())
    #print('>', show.start_time>datetime.datetime.now())
    #print('<', show.start_time<datetime.datetime.now())
    if show.start_time<datetime.datetime.now():
      past_shows_count+=1
      show_dict={}
      show_dict['id']=show.id
      show_artist = Artist.query.get(show.artist_id)
      show_dict['artist_name']=show_artist.name
      show_dict['artist_image_link']=show_artist.image_link
      show_dict['start_time']=show.start_time.strftime("%A %d. %B %Y")
      past_shows_list.append(show_dict.copy())
    if show.start_time>datetime.datetime.now():
      upcoming_shows_count+=1
      show_dict={}
      show_dict['id']=show.id
      show_artist = Artist.query.get(show.artist_id)
      show_dict['artist_name']=show_artist.name
      show_dict['artist_image_link']=show_artist.image_link
      show_dict['start_time']=show.start_time.strftime("%A %d. %B %Y")
      upcoming_shows_list.append(show_dict.copy())
  ven_dict['past_shows']=past_shows_list
  ven_dict['upcoming_shows']=upcoming_shows_list
  ven_dict['past_shows_count']=past_shows_count
  ven_dict['upcoming_shows_count']=upcoming_shows_count
  #print("dbase", ven_dict)
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  #print("hard coded", data)
  return render_template('pages/show_venue.html', venue=ven_dict)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # This is basically copy and pasted from an answer by Juliano V.
  # I tried to use the lesson but it emphasized the need to have the "name" attribute in the form
  # That does not exist in this form and nothing else seems to correspond to the lesson
  # I have added comments
  form = VenueForm(request.form, meta={'csrf': False}) # I have seen references to this on the forum 
  #form = VenueForm(request.form) # testing if I need csrf
  if form.validate(): # This I missed if it was presented and am just using from Juliano
      try:
          venue = Venue(
              name=form.name.data, # These do not refer to the name attribute which was emphasized
              city=form.city.data, 
              state=form.state.data,
              address=form.address.data,
              phone=form.phone.data,
              genres=form.genres.choices,
              facebook_link=form.facebook_link.data,
              image_link=form.image_link.data,
              website=form.website.data,
              seeking_talent=form.seeking_talent.data,
              seeking_description=form.seeking_description.data
          )
          db.session.add(venue) # These were in the lesson
          db.session.commit() # And this complets the database cycle per lesson
          flash('Venue ' + form.name.data + ' was successfully listed!')
      except ValueError as e: # Try Fail was also in the lesson, so this makes sense
          print(e)
          flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  else:
      message = []
      for f, e in form.errors.items():
          message.append(f + ' ' + '|'.join(e))
      flash('Errors ' + str(message))
  return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  artists = Artist.query.all()
  art_list=[]
  for artist in artists:
    art_dict = {}
    art_dict['id']=artist.id
    art_dict['name']=artist.name
    art_list.append(art_dict.copy())
  return render_template('pages/artists.html', artists=art_list)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  artist = Artist.query.get(artist_id)
  art_dict = {}
  art_dict['id']=artist.id
  art_dict['name']=artist.name
  art_dict['genres']=artist.genres
  art_dict['city']=artist.city
  art_dict['state']=artist.state
  art_dict['phone']=artist.phone
  art_dict['seeking_venue']=artist.seeking_venue
  art_dict['image_link']=artist.image_link
  past_shows_list=[]
  upcoming_shows_list=[]
  past_shows_count = 0
  upcoming_shows_count = 0
  for show in Show.query.filter_by(artist_id=artist.id):
    show_dict = {}
    #print('these shows', show.id, show.start_time)
    #print('now it is:', datetime.datetime.now())
    #print('>', show.start_time>datetime.datetime.now())
    #print('<', show.start_time<datetime.datetime.now())
    show_dict['id']=show.id
    venue_show = Venue.query.get(show.venue_id)
    show_dict['venue_id']=venue_show.id
    show_dict['venue_name']=venue_show.name
    show_dict['venue_image_line']=venue_show.image_link
    show_dict['start_time']=show.start_time.strftime("%A %d. %B %Y")
    if show.start_time<datetime.datetime.now():
      past_shows_count+=1
      past_shows_list.append(show_dict.copy())
    if show.start_time>datetime.datetime.now():
      upcoming_shows_count+=1
      upcoming_shows_list.append(show_dict.copy())
  art_dict['past_shows']=past_shows_list
  art_dict['upcoming_shows']=upcoming_shows_list
  art_dict['past_shows_count']=past_shows_count
  art_dict['upcoming_shows_count']=upcoming_shows_count

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=art_dict)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  art_dict = {}
  art_dict['id']=artist.id
  art_dict['name']=artist.name
  art_dict['genres']=artist.genres
  art_dict['city']=artist.city
  art_dict['state']=artist.state
  art_dict['phone']=artist.phone
  art_dict['website']=artist.website
  art_dict['facebook_link']=artist.facebook_link
  art_dict['seeking_venue']=artist.seeking_venue
  art_dict['seeking_description']=artist.seeking_description
  art_dict['image_link']=artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=art_dict)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form, meta={'csrf': False}) # I have seen references to this on the forum 
  #form = VenueForm(request.form) # testing if I need csrf
  if form.validate(): # This I missed if it was presented and am just using from Juliano
      try:
          artist = Artist(
              name=form.name.data, # These do not refer to the name attribute which was emphasized
              city=form.city.data, 
              state=form.state.data,
              phone=form.phone.data,
              genres=form.genres.choices,
              facebook_link=form.facebook_link.data,
              image_link=form.image_link.data,
              website=form.website.data,
              seeking_venue=form.seeking_talent.data,
              seeking_description=form.seeking_description.data
          )
          db.session.add(artist) # These were in the lesson
          db.session.commit() # And this complets the database cycle per lesson
          flash('Artist ' + form.name.data + ' was successfully listed!')
      except ValueError as e: # Try Fail was also in the lesson, so this makes sense
          print(e)
          flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  else:
      message = []
      for f, e in form.errors.items():
          message.append(f + ' ' + '|'.join(e))
      flash('Errors ' + str(message))
  return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!') Alternative variable to flash name
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  shows=Show.query.all()
  show_list = []
  for show in shows:
    show_dict={}
    venue=Venue.query.get(show.venue_id)
    show_dict['venue_id']=venue.id
    show_dict["venue_name"]=venue.name
    artist = Artist.query.get(show.artist_id)
    show_dict['artist_id']=artist.id
    show_dict['artist_name']=artist.name
    show_dict['artist_image_link']=artist.image_link
    show_dict['start_time']=show.start_time.strftime("%A %d. %B %Y")
    show_list.append(show_dict.copy())
  return render_template('pages/shows.html', shows=show_list)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
