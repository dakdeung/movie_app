from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie, MovieSchema

def read_all():

    # Create the list of people from our data
    director = Director.query.order_by(Director.id).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def read_one(id):

    # Get the person requested
    director = Director.query.filter(Director.id == id).one_or_none()


    # Did we find a person?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Director not found for Id: {id}".format(id=id),
        )

def create(director):

    uid = director.get("uid")

    existing_director = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )


    # Can we insert this person?
    if existing_director is None:

        # Create a person instance using the schema and the passed in person
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the person to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_director)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Director {uid} exists already not found".format(
                uid=uid
            ),
        )

def update(id, director):

    # Get the person requested from the db into session
    update_director = Director.query.filter(
        Director.id == id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    uid = director.get("uid")

    existing_director = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_director is None:
        abort(
            404,
            "Director not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_director is not None and existing_director.id != id
    ):
        abort(
            409,
            "Director {uid} exists already".format(
                uid=uid
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the person we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_director)

        return data, 200


def delete(id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    director = Director.query.filter(Director.id == id).one_or_none()

    # Did we find a person?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(
            "Director {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Director not found for Id: {id}".format(id=id),
        )