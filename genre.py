from config import db
from models import Genre, GenreSchema, Movie
from mapper import Reponse
from validator_body import validator_body

def read_all():
    """
    This function read_all a genre from the genres structure
    :return:            200 on successful read_all
    """
    # Create the list of genres from our data
    genre = Genre.query.order_by(Genre.id).limit(15).all()

    # Serialize the data for the response
    genre_schema = GenreSchema(many=True)
    data = genre_schema.dump(genre)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):
    """
    This function read_one a genre from the genres structure
    :param id:          Id of the genre to get data
    :return:            200 on successful read_all
    """
    # Get the genre requested
    genre = Genre.query.filter(Genre.id == id).one_or_none()


    # Did we find a genre?
    if genre is not None:

        # Serialize the data for the response
        genre_schema = GenreSchema()
        data = genre_schema.dump(genre)
        return Reponse(200,"Get Succesfully",[],data)

    # Otherwise, nope, didn't find that genre
    else:
        return Reponse(404,"Genre not found for Id: {id}".format(id=id),[],{})

def create(genre):
    """
    This function create a genre from the genres structure
    :body genre:        Body of the genre to Create data
    :return:            200 on successful read_all 404 Id genre not found, 409 body false
    """
    # set varibale
    name = genre.get('name')
    movie = genre.get("movie")

    # check existing genre in database
    existing_genre = (
        Genre.query.filter(Genre.name == name)
        .one_or_none()
    )

    # check body value 
    validate_body = validator_body.genre_required(genre)

    # Can we insert this genre?
    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    else:
        check_movie = validator_body.check_movie_value(genre)
        if existing_genre is not None:
            return Reponse(404,"Genre {name} already exists ".format(name=name),[],{})
        elif check_movie[0]:
            return Reponse(409,"Movie {not_found} not found".format(not_found=check_movie[1]),[],{})
        # Otherwise, nope, genre exists already
        else:
            # Create a genre instance using the schema and the passed in genre
            schema = GenreSchema()
            # Add the genre to the database
            new_genre = schema.load(genre, session=db.session)
            # looping genre
            for i in movie:
                # find movie by id
                value = Movie.query.filter(Movie.id == i).one_or_none()
                # add movie into genre 
                new_genre.movies.append(value)
                db.session.commit()
            # Add the genre to the database
            db.session.add(new_genre)
            db.session.commit()

            # Serialize and return the newly created genre in the response
            data = schema.dump(new_genre)

            return Reponse(201,"Created Succesfully",[],data)
        

def update(id, genre):
    """
    This function update a genre from the genres structure
    :param id:          Id of the genre to update
    :body genre:        Body of the genre to update data
    :return:            200 on successful delete, 404 if not found, 409 body false
    """
    # set varibale
    name = genre.get('name')
    movie = genre.get("movie")

    # Get the genre requested from the db into session
    update_genre = Genre.query.filter(
        Genre.id == id
    ).one_or_none()

    # Try to find an existing genre with the same name as the update
    uid = genre.get("name")

    existing_genre = (
        Genre.query.filter(Genre.name == name)
        .one_or_none()
    )

    # check body value
    validate_body = validator_body.genre_required(genre)    

    # Are we trying to find a genre that does not exist?
    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    else:
        check_movie = validator_body.check_movie_value(genre)
        if update_genre is None:
            return Reponse(404,"Genre not found for Id: {id}".format(id=id),[],{})
        elif check_movie[0]:
            return Reponse(409,"Genre {not_found} not found".format(not_found=check_movie[1]),[],{})
        # Would our update create a duplicate of another genre already existing?
        elif (
            existing_genre is not None and existing_genre.id != id
        ):
            return Reponse(409,"Genre {name} exists already".format(name=name),[],{})

        # Otherwise go ahead and update!
        else:
            # turn the passed in genre into a db object
            schema = GenreSchema()
            update = schema.load(genre, session=db.session)

            # Set the id to the genre we want to update
            update.id = update_genre.id
            # looping genre
            for i in movie:
                # find movie by id
                value = Movie.query.filter(Movie.id == i).one_or_none()
                # add movie into genre 
                update.movies.append(value)
                db.session.commit()
            # merge the new object into the old and commit it to the db
            db.session.merge(update)
            db.session.commit()

            # return updated genre in the response
            data = schema.dump(update_genre)

            return Reponse(200,"Update Successfully",[],data)


def delete(id):
    """
    This function deletes a genre from the genres structure
    :param id:          Id of the genre to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the genre requested
    genre = Genre.query.filter(Genre.id == id).one_or_none()

    # Did we find a genre?
    if genre is not None:
        db.session.delete(genre)
        db.session.commit()
        return Reponse(200,"Genre {id} deleted".format(id=id),[],{})

    # Otherwise, nope, didn't find that genre
    else:
        return Reponse(200,"Genre not found for Id: {id}".format(id=id).format(id=id),[],{})