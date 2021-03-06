#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import collections
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
collections.Callable = collections.abc.Callable

migrate=Migrate(app,db)




# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


venue_genrs=db.Table('venue_genrs',db.Column('venue_id',db.Integer,db.ForeignKey('Venue.id'),primary_key=True),db.Column('genre_id',db.Integer,db.ForeignKey('Genre.id'),primary_key=True))


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String(120))
    city=db.Column(db.String())
    state=db.Column(db.String())
    phone = db.Column(db.String(120))
    website=db.Column(db.String(150))
    seeking_talent=db.Column(db.Boolean)
    seeking_description=db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    create_dt=db.Column(db.DateTime)
    #city_id=db.Column(db.Integer,db.ForeignKey("City.id"))
    show=db.relationship("Show",backref='venue')
    genres=db.relationship('Genre',secondary=venue_genrs,backref=db.backref('venues',lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

artist_genrs=db.Table('artist_genrs',db.Column('artist_id',db.Integer,db.ForeignKey('Artist.id'),primary_key=True),db.Column('genre_id',db.Integer,db.ForeignKey('Genre.id'),primary_key=True))

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city=db.Column(db.String)
    state=db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website=db.Column(db.String(150))
    facebook_link = db.Column(db.String(120))
    seeking_venue=db.Column(db.Boolean)
    seeking_description=db.Column(db.String())
    image_link=db.Column(db.String())
    create_dt=db.Column(db.DateTime)
    show=db.relationship("Show",backref='artist')
    genres=db.relationship('Genre',secondary=artist_genrs,backref=db.backref('artists',lazy=True))





    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id=db.Column(db.Integer,primary_key=True)
  artist_id=db.Column(db.Integer,db.ForeignKey("Artist.id"))
  venue_id=db.Column(db.Integer,db.ForeignKey("Venue.id"))
  start_time=db.Column(db.DateTime)
  is_upcoming=db.Column(db.Boolean)




class Genre(db.Model):
  __tablename__ = 'Genre'

  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(120),nullable=False)


class City(db.Model):
  __tablename__ = 'City'

  id=db.Column(db.Integer,primary_key=True)
  city=db.Column(db.String(120),nullable=False)
  state=db.Column(db.String(120),nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():

  #Recently Added Venue and Artist

  new_artists=Artist.query.order_by(Artist.create_dt).limit(10).all()
  new_venues=Venue.query.order_by(Venue.create_dt).limit(10).all()

  return render_template('pages/home.html',venues=new_venues,artists=new_artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 

  data=[]
  vv=[]

  city=Venue.query.add_columns(Venue.city,Venue.state).distinct(Venue.city,Venue.state)
  #res={'vv':[]}
  venue=Venue.query.add_columns(Venue.id,Venue.name,Venue.city)



  for c in city:
    for v in venue:
      if c.city == v.city:
        vv.append({'id':v.id,'name':v.name})
    data.append({'city':c.city,'state':c.state,'venues':vv})
    vv=[]




  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  term=request.form.get('search_term', '')
  res=Venue.query.filter(Venue.name.ilike(f'%{term}%'))
  response['data']=res.all()
  response["count"]=res.count()
  return render_template('pages/search_venues.html', results=response, search_term=term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  
  
  data=Venue.query.get(venue_id)
  collections.Callable = collections.abc.Callable

  u_c=0
  p_s=0

  past_s=[]
  upcoming_s=[]
# Iterating each shows and create  atrists in past and upcoming shows
  for show in data.show:
    if show.is_upcoming==True:
      arts=show.query.join(Artist)
      for a in arts:
        if a.id == show.id:
          upcoming_s.append({"artist_id": a.artist.id,
      "artist_name":a.artist.name,
      "artist_image_link":a.artist.image_link,
      "start_time": show.start_time,'is_upcoming':True})
      u_c=u_c+1
    else:
      arts=show.query.join(Artist)
      for a in arts:
        if a.id == show.id:
          past_s.append({"artist_id": a.artist.id,
      "artist_name":a.artist.name,
      "artist_image_link":a.artist.image_link,
      "start_time": show.start_time,'is_upcoming':False})
      p_s=p_s+1
  
  data.upcoming_shows_count=u_c
  data.past_shows_count=p_s
  data.past_shows=past_s
  data.upcoming_shows=upcoming_s

  

  return render_template('pages/show_venue.html', venue=data)

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
  err=False
  v={}
  try:
    name = request.form['name']
    v['name']=name

    genres=request.form.getlist('genres')

    gs=[]

    for g in genres:
      gs.append(Genre(name=g))



    



    if request.form['seeking_talent']=='y':
      seeking_talent=True
    else:
      seeking_talent=False
    venue=Venue(name=name,
    city=request.form['city'],state=request.form['state'],
    address=request.form['address'],phone=request.form['phone'],
    image_link=request.form['image_link'],facebook_link=request.form['facebook_link'],
    website=request.form['website_link'],seeking_talent=seeking_talent,
    seeking_description=request.form['seeking_description'])
    g=Genre(name=request.form['genres'])
    venue.genres=gs
    db.session.add(venue)
    db.session.commit()
  except:
    v['name']=request.form['name']
    db.session.rollback()
    err=True
  finally:
    db.session.close()
  
  if err == False:
    flash('Venue ' + v['name'] + ' was successfully listed!')
  else:
    flash('An error occurred ' + v['name'] + ' could not be listed!')


  return render_template('pages/home.html')


  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  #Personal Note
  # AJAX fetch is used in the front end to this endpoint.
  try:
    venue=Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  

  data=Artist.query.add_columns(Artist.id,Artist.name).all()
  return render_template('pages/artists.html', artists=data)

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

  term=request.form.get('search_term', '')
  res=Artist.query.filter(Artist.name.ilike(f'%{term}%'))
  response['data']=res.all()
  response["count"]=res.count()
  return render_template('pages/search_artists.html', results=response, search_term=term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
 
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  data=Artist.query.get(artist_id)

  u_c=0
  p_s=0

  past_s=[]
  upcoming_s=[]

  # Iterating each shows and create past and upcoming venues

  for show in data.show:
    if show.is_upcoming==True:
      arts=show.query.join(Venue)
      for a in arts:
        if a.id == show.id:
          upcoming_s.append({"venue_id": a.artist.id,
      "venue_name":a.artist.name,
      "venue_image_link":a.artist.image_link,
      "start_time": show.start_time,'is_upcoming':True})
      u_c=u_c+1
    else:
      arts=show.query.join(Venue)
      for a in arts:
        if a.id == show.id:
          past_s.append({"venue_id": a.artist.id,
      "venue_name":a.artist.name,
      "venue_image_link":a.artist.image_link,
      "start_time": show.start_time,'is_upcoming':False})
      p_s=p_s+1
  
  data.upcoming_shows_count=u_c
  data.past_shows_count=p_s
  data.past_shows=past_s
  data.upcoming_shows=upcoming_s
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # TODO: populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  genres=request.form.getlist('genres')

  gs=[]

  for g in genres:
    gs.append(Genre(name=g))

  artist=Artist.query.get(artist_id)
  artist.name=request.form['name']
  artist.address=request.form['address']
  artist.phone=request.form['phone']
  artist.city=request.form['city']
  artist.state=request.form['state']
  artist.website=request.form['website_link']
  artist.facebook_link=request.form['facebook_link']
  artist.seeking_talent=request.form['seeking_talent']
  artist.seeking_description=request.form['seeking_description']
  artist.image_link=request.form['image_link']
  artist.genres=gs

  db.session.add(artist)
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue=Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  genres=request.form.getlist('genres')

  gs=[]

  for g in genres:
    gs.append(Genre(name=g))

  venue=Venue.query.get(venue_id)
  venue.name=request.form['name']
  venue.address=request.form['address']
  venue.phone=request.form['phone']
  venue.city=request.form['city']
  venue.state=request.form['state']
  venue.website=request.form['website_link']
  venue.facebook_link=request.form['facebook_link']
  venue.seeking_talent=request.form['seeking_talent']
  venue.seeking_description=request.form['seeking_description']
  venue.image_link=request.form['image_link']
  venue.genres=gs

  db.session.add(venue)
  db.session.commit()

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

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  

  data=Show.query.all()
  show=[]
  collections.Callable = collections.abc.Callable

  for d in data:
    show.append({'venue_id':d.venue.id,'venue_name':d.venue.name,
    'artist_id':d.artist.id,'artist_name':d.artist.name,
    'artist_image_link':d.artist.image_link,'start_time':d.start_time.strftime("%m/%d/%Y, %H:%M:%S")})


  return render_template('pages/shows.html', shows=show)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  err=False
  try:
    v_id=request.form['venue_id']
    a_id=request.form['artist_id']
    s_time=request.form['start_time']
    show=Show(venue_id=v_id,artist_id=a_id,start_time=s_time)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    err=True
  finally:
    db.session.close()
  
  if err:
    flash('An error occurred. Show could not be listed!')
  else:
    flash('Show was successfully listed!')

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
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
