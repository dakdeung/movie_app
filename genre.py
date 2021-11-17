from config import db
from models import Genre, GenreSchema
from mapper import Reponse
from validator_body import validator_body

def read_all():

    # Create the list of people from our data
    genre = Genre.query.order_by(Genre.id).limit(15).all()

    # Serialize the data for the response
    genre_schema = GenreSchema(many=True)
    data = genre_schema.dump(genre)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):
    
    # Get the person requested
    genre = Genre.query.filter(Genre.id == id).one_or_none()


    # Did we find a person?
    if genre is not None:

        # Serialize the data for the response
        genre_schema = GenreSchema()
        data = genre_schema.dump(genre)
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(404,"Genre not found for Id: {id}".format(id=id),[],{})

def create(genre):

    name = genre.get('name')
    existing_genre = (
        Genre.query.filter(Genre.name == name)
        .one_or_none()
    )

    validate_body = validator_body.genre_required(genre)

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Can we insert this person?
    elif existing_genre is not None:

        return Reponse(404,"Genre {name} already exists ".format(name=name),[],{})

    # Otherwise, nope, person exists already
    else:
        # Create a person instance using the schema and the passed in person
        schema = GenreSchema()
        new_genre = schema.load(genre, session=db.session)

        # Add the person to the database
        db.session.add(new_genre)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_genre)

        return Reponse(201,"Created Succesfully",[],data)
        

def update(id, genre):

    name = genre.get('name')
    # Get the person requested from the db into session
    update_genre = Genre.query.filter(
        Genre.id == id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    uid = genre.get("name")

    existing_genre = (
        Genre.query.filter(Genre.name == name)
        .one_or_none()
    )

    validate_body = validator_body.genre_required(genre)    

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Are we trying to find a person that does not exist?
    elif update_genre is None:
        return Reponse(404,"Genre not found for Id: {id}".format(id=id),[],{})

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_genre is not None and existing_genre.id != id
    ):
        return Reponse(409,"Genre {uid} exists already".format(uid=uid),[],{})

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = GenreSchema()
        update = schema.load(genre, session=db.session)

        # Set the id to the person we want to update
        update.id = update_genre.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_genre)

        return Reponse(200,"Update Successfully",[],data)


def delete(id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    genre = Genre.query.filter(Genre.id == id).one_or_none()

    # Did we find a person?
    if genre is not None:
        db.session.delete(genre)
        db.session.commit()
        return Reponse(200,"Genre {id} deleted".format(id=id),[],{})

    # Otherwise, nope, didn't find that person
    else:
        return Reponse(200,"Genre not found for Id: {id}".format(id=id).format(id=id),[],{})