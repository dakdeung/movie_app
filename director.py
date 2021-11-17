from flask import make_response, abort
from config import db
from models import Director, DirectorSchema
from mapper import Reponse
from validator_body import validator_body

def read_all():

    # Create the list of people from our data
    director = Director.query.order_by(Director.id).limit(15).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):

    # Get the person requested
    director = Director.query.filter(Director.id == id).one_or_none()


    # Did we find a person?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Director not found for Id: {id}".format(id=id),[],{})

def create(director):

    uid = director.get("uid")

    existing_director = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )


    validate_body = validator_body.director_required(director)

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Can we insert this person?
    elif existing_director is not None:

        return Reponse(404,"Director with UID {uid} already exists ".format(uid=uid),[],{})

    # Otherwise, nope, person exists already
    else:
        # Create a person instance using the schema and the passed in person
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the person to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_director)

        return Reponse(201,"Created Succesfully",[],data)
        

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

    validate_body = validator_body.director_required(director)    

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Are we trying to find a person that does not exist?
    elif update_director is None:
        return Reponse(404,"Director not found for Id: {id}".format(id=id),[],{})

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_director is not None and existing_director.id != id
    ):
        return Reponse(409,"Director {uid} exists already".format(uid=uid),[],{})

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

        return Reponse(200,"Update Successfully",[],data)


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
        return Reponse(200,"Director {id} deleted".format(id=id),[],{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(200,"Director not found for Id: {id}".format(id=id).format(id=id),[],data)