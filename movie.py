from os import name
from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema, Genre, GenreSchema
from mapper import Reponse
from validator_body import validator_body

def read_all():

    # Create the list of people from our data
    movie = Movie.query.order_by(Movie.id).limit(15).all()

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):

    # Get the person requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a person?
    if movie is not None:

        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        
        return Reponse(200,"Get Succesfully",[],data)

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def read_top(limit,key):
    
    if key == 'vote':
        # Get the person requested
        movie = Movie.query.order_by(Movie.vote_average.desc()).limit(limit).all()
    elif key == 'popularity':
        movie = Movie.query.order_by(Movie.popularity.desc()).limit(limit).all()
    else:
        return Reponse(200,"Key only can popularity or vote",[],{})

    # Did we find a person?
    if movie is not None:

        print(movie)
        # Serialize the data for the response
        movie_schema = MovieSchema(many=True)
        data = movie_schema.dump(movie)

        print(data)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def read_release(start,end):
    
    validate_date = validator_body.check_date(start,end)

    if end is None:
        movie = Movie.query.filter(Movie.release_date == start).order_by(Movie.release_date.desc()).all()
    else:
        movie = Movie.query.filter(Movie.release_date.between(start, end)).order_by(Movie.release_date.desc()).all()

    if validate_date:
        return Reponse(409,"Format date wrong (YYYY/MM/DD)",[],{})
    # Did we find a person?
    elif movie is not None:

        print(movie)
        # Serialize the data for the response
        movie_schema = MovieSchema(many=True)
        data = movie_schema.dump(movie)

        print(data)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})
  

def create(movie):

    title = movie.get("title")
    director_id = movie.get("director_id")
    uid = movie.get("uid")
    id_genre = movie.get("genre")

    name_genre = Genre.query.filter(Genre.id == id_genre).one_or_none()

    existing_movie = (
        Movie.query.filter(Movie.title == title)
        .one_or_none()
    )

    existing_directors = (
        Director.query.filter(Director.id == director_id).one_or_none()
    )

    existing_uid = (
        Director.query.filter(Director.uid == uid).one_or_none()
    )

    validate_body = validator_body.movie_required(movie)

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Can we insert this person?
    elif existing_movie is not None:
        return Reponse(409,"Movie {title} exists already".format(title=title),[],{})

    elif existing_directors is None:
        return Reponse(409,"Director Id not found",[],{})
    elif existing_uid is not None:
        return Reponse(409,"Movie with UID {uid} exists already",[],{})
    # Otherwise, nope, person exists already
    else:
        # Create a person instance using the schema and the passed in person
        schema = MovieSchema()
        

        # Add the person to the database
        # db.session.add(new_movie)
        
        movie = schema.load(movie, session=db.session)
        movie.genres.append(name_genre)
        db.session.add(movie)
        db.session.commit()
        

        # Serialize and return the newly created person in the response
        data = schema.dump(movie)

        return Reponse(201,"Created Succesfully",[],data)

def update(id, movie):

    # Get the person requested from the db into session
    update_movie = Movie.query.filter(
        Movie.id == id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    title = movie.get("title")
    director_id = movie.get("director_id")
    uid = movie.get("uid")

    existing_movie = (
        Movie.query.filter(Movie.title == title)
        .one_or_none()
    )

    existing_uid = (
        Director.query.filter(Director.uid == uid).one_or_none()
    )

    existing_directors = (
        Director.query.filter(Director.id == director_id).one_or_none()
    )

    validate_body = validator_body.movie_required(movie)

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Are we trying to find a person that does not exist?
    elif update_movie is None:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

    elif existing_uid is not None:
        return Reponse(409,"Movie with UID {uid} exists already",[],{})

    elif existing_directors is None:
        return Reponse(409,"Director Id not found",[],{})
    # Would our update create a duplicate of another person already existing?
    elif (existing_movie is not None and existing_movie.id != id):
        return Reponse(404,"Movie {title} exists already".format(title=title),[],{})

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id to the person we want to update
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_movie)

        return Reponse(200,"Update Succesfully",data,{})


def delete(id):

    # Get the person requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a person?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return Reponse(200,"Movie {id} deleted".format(id=id),[],{})
        

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})