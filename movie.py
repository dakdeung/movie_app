from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema, Genre
from mapper import Reponse
from validator_body import validator_body

def read_all():
    """
    This function read_all a movie from the movies structure
    :return:            200 on successful read_all
    """
    # Create the list of movies from our data
    movie = Movie.query.order_by(Movie.id).limit(15).all()

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):
    """
    This function read_one a movie from the movies structure
    :param id:          Id of the movie to get data
    :return:            200 on successful read_all
    """
    # Get the movie requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a movie?
    if movie is not None:

        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        
        return Reponse(200,"Get Succesfully",[],data)

    # Otherwise, nope, didn't find that movie
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def read_top(limit,key):
    """
    This function read_top a movie from the movies structure to get top movie
    :param id   :       Id of the movie to get data
        limit   :       limit of limit the data to show data
        key     :       key of category only can vote or popularity
    :return:            200 on successful read_all 404 Id movie not found
    """
    # Get the movie requested
    if key == 'vote':
        movie = Movie.query.order_by(Movie.vote_average.desc()).limit(limit).all()
    elif key == 'popularity':
        movie = Movie.query.order_by(Movie.popularity.desc()).limit(limit).all()
    else:
        return Reponse(200,"Key only can popularity or vote",[],{})

    # Did we find a movie?
    if movie is not None:
        # Serialize the data for the response
        movie_schema = MovieSchema(many=True)
        data = movie_schema.dump(movie)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that movie
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def read_release(start,end):
    """
    This function read_top a movie from the movies structure
    :param id   :       Id of the movie to get data
        start   :       start of date to query the data
        end     :       end of date to query the data
    :return:            200 on successful read_all 404 Id movie not found
    """
    # variable to check body with format date
    validate_date = validator_body.check_date(start,end)

    # check date
    if end is None:
        movie = Movie.query.filter(Movie.release_date == start).order_by(Movie.release_date.desc()).all()
    else:
        movie = Movie.query.filter(Movie.release_date.between(start, end)).order_by(Movie.release_date.desc()).all()

     # Did we find a movie?
    if validate_date:
        return Reponse(409,"Format date wrong (YYYY/MM/DD)",[],{})
    elif movie is not None:
        # Serialize the data for the response
        movie_schema = MovieSchema(many=True)
        data = movie_schema.dump(movie)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that movie
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})
  

def create(movie):
    """
    This function create a movie from the movies structure
    :body movie:        Body of the movie to Create data
    :return:            200 on successful read_all 404 Id movie not found, 409 body false
    """
    # set variable
    title = movie.get("title")
    director_id = movie.get("director_id")
    uid = movie.get("uid")
    genre = movie.get("genre")

    # check existing data
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

    # variable to check body with value not none
    validate_body = validator_body.movie_required(movie)
    

    # Can we insert this movie?
    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    else:
        check_genre = validator_body.check_genre_value(movie)
        if existing_movie is not None:
            return Reponse(409,"Movie {title} exists already".format(title=title),[],{})
        elif check_genre[0]:
            return Reponse(409,"Genre {not_found} not found".format(not_found=check_genre[1]),[],{})
        elif existing_directors is None:
            return Reponse(409,"Director Id not found",[],{})
        elif existing_uid is not None:
            return Reponse(409,"Movie with UID {uid} exists already",[],{})
        # Otherwise, nope, movie exists already
        else:
            # Create a movie instance using the schema and the passed in movie
            schema = MovieSchema()
            # Add the movie to the database
            new_movie = schema.load(movie, session=db.session)
            # looping genre
            for i in genre:
                # find genre by id
                value = Genre.query.filter(Genre.id == i).one_or_none()
                # add genre into movie 
                new_movie.genres.append(value)
                db.session.commit()
            # add and commit db
            db.session.add(new_movie)
            db.session.commit()        

            # Serialize and return the newly created movie in the response
            data = schema.dump(new_movie)

            return Reponse(201,"Created Succesfully",[],data)

def update(id, movie):
    """
    This function update a movie from the movies structure
    :param id:          Id of the movie to update
    :body movie:        Body of the movie to update data
    :return:            200 on successful delete, 404 if not found, 409 body false
    """
    
    # Get the movie requested from the db into session
    update_movie = Movie.query.filter(
        Movie.id == id
    ).one_or_none()

    # set variable
    title = movie.get("title")
    director_id = movie.get("director_id")
    uid = movie.get("uid")
    genre = movie.get("genre")
    count_genre = 0
    
    # check existing data
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

    # variable to check body with value not none
    validate_body = validator_body.movie_required(movie)

    # Are we trying to find a movie that does not exist?
    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    else:
        check_genre = validator_body.check_genre_value(movie)
        if update_movie is None:
            return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})
        elif check_genre[0]:
            return Reponse(409,"Genre {not_found} not found".format(not_found=check_genre[1]),[],{})
        elif existing_uid is not None:
            return Reponse(409,"Movie with UID {uid} exists already",[],{})
        elif existing_directors is None:
            return Reponse(409,"Director Id not found",[],{})
        # Would our update create a duplicate of another movie already existing?
        elif (existing_movie is not None and existing_movie.id != id):
            return Reponse(404,"Movie {title} exists already".format(title=title),[],{})

        # Otherwise go ahead and update!
        else:

            # turn the passed in movie into a db object
            schema = MovieSchema()
            update = schema.load(movie, session=db.session)

            # Set the id to the movie we want to update
            # update.id = update_movie.id
            # looping genre
            for i in genre:
                # find genre by id
                value = Genre.query.filter(Genre.id == i).one_or_none()
                # add genre to movie
                update.genres.append(value)
                db.session.commit()
            # merge the new object into the old and commit it to the db
            db.session.merge(update)
            db.session.commit()

            # return updated person in the response
            data = schema.dump(update_movie)

            return Reponse(200,"Update Succesfully",data,{})


def delete(id):
    """
    This function deletes a movie from the movies structure
    :param id:          Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return Reponse(200,"Movie {id} deleted".format(id=id),[],{})
        

    # Otherwise, nope, didn't find that movie
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})