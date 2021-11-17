"""
This is the people module and supports all the REST actions for the
people data
"""
from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema

def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    movie = Movie.query.order_by(Movie.id).all()

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return data

def read_one(id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people
    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Get the person requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a person?
    if movie is not None:

        # Serialize the data for the response
        person_schema = MovieSchema()
        data = person_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Movie not found for Id: {id}".format(id=id),
        )

def create(movie):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    title = movie.get("title")
    director_id = movie.get("director_id")

    existing_movie = (
        Movie.query.filter(Movie.title == title)
        .one_or_none()
    )

    existing_directors = (
        Director.query.filter(Director.id == director_id).one_or_none()
    )

    # Can we insert this person?
    if existing_movie is None and existing_directors is not None:

        # Create a person instance using the schema and the passed in person
        schema = MovieSchema()
        new_movie = schema.load(movie, session=db.session)

        # Add the person to the database
        db.session.add(new_movie)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_movie)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Movie {title} exists already or Director Id not found".format(
                title=title
            ),
        )

def update(id, movie):
    """
    This function updates an existing person in the people structure
    Throws an error if a person with the name we want to update to
    already exists in the database.
    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_movie = Movie.query.filter(
        Movie.id == id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    title = movie.get("title")

    existing_movie = (
        Movie.query.filter(Movie.title == title)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_movie is None:
        abort(
            404,
            "Movie not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_movie is not None and existing_movie.id != id
    ):
        abort(
            409,
            "Movie {title} exists already".format(
                title=title
            ),
        )

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

        return data, 200


def delete(id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Did we find a person?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Movie not found for Id: {id}".format(id=id),
        )