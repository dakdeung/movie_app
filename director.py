from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie
from mapper import Reponse
from validator_body import validator_body

def read_all():
    """
    This function read_all a director from the directors structure
    :return:            200 on successful read_all
    """

    # Create the list of directors from our data
    director = Director.query.order_by(Director.id).limit(15).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return Reponse(200,"Get All Succesfully",data,{})

def read_one(id):
    """
    This function read_one a director from the directors structure
    :param id:          Id of the director to get data
    :return:            200 on successful read_all
    """
    # Get the director requested
    director = Director.query.filter(Director.id == id).one_or_none()


    # Did we find a director?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return Reponse(200,"Get Succesfully",[],data)

    # Otherwise, nope, didn't find that director
    else:
        return Reponse(404,"Director not found for Id: {id}".format(id=id),[],{})

def read_top(id,limit,key):
    """
    This function read_top a director from the directors structure to get top director
    :param id   :       Id of the director to get data
        limit   :       limit of limit the data to show data
        key     :       key of category only can vote or popularity
    :return:            200 on successful read_all 404 Id director not found
    """

    # Get the director requested
    if key == 'vote':
        director = Director.query.join(Movie, Movie.director_id == Director.id).filter(Director.id == id).filter(Movie.director_id == id).order_by(Movie.vote_average.desc()).limit(limit).all()
    elif key == 'popularity':
        director = Director.query.join(Movie, Movie.director_id == Director.id).filter(Director.id == id).filter(Movie.director_id == id).order_by(Movie.popularity.desc()).limit(limit).all()
    else:
        return Reponse(200,"Key only can popularity or vote",[],{})

    # Did we find a director?
    if director is not None:

        print(director)
        # Serialize the data for the response
        director_schema = DirectorSchema(many=True)
        data = director_schema.dump(director)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that director
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def read_release(id,start,end):
    """
    This function read_top a director from the directors structure
    :param id   :       Id of the director to get data
        start   :       start of date to query the data
        end     :       end of date to query the data
    :return:            200 on successful read_all 404 Id director not found
    """

    # variable to check body with format date
    validate_date = validator_body.check_date(start,end)

    # check date
    if end is None:
        director = Director.query.filter(Director.id == id).filter(Movie.director_id == id).join(Movie, Movie.director_id == Director.id).filter(Movie.release_date == start).order_by(Movie.release_date.desc()).all()
    else:
        director = Director.query.filter(Director.id == id).filter(Movie.director_id == id).join(Movie, Movie.director_id == Director.id).filter(Movie.release_date.between(start, end)).order_by(Movie.release_date.desc()).all()

    # Did we find a directors?
    if validate_date:
        return Reponse(409,"Format date wrong (YYYY/MM/DD)",[],{})
    elif director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema(many=True)
        data = director_schema.dump(director)

        print(data)
        
        return Reponse(200,"Get Succesfully",data,{})

    # Otherwise, nope, didn't find that directors
    else:
        return Reponse(404,"Movie not found for Id: {id}".format(id=id),[],{})

def create(director):
    """
    This function create a director from the directors structure
    :body director:     Body of the director to Create data
    :return:            200 on successful read_all 404 Id director not found, 409 body false
    """

    # set variable
    uid = director.get("uid")

    # check existing director
    existing_director = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )

    # variable to check body with value not none
    validate_body = validator_body.director_required(director)

    # Can we insert this director?
    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    elif existing_director is not None:

        return Reponse(404,"Director with UID {uid} already exists ".format(uid=uid),[],{})

    # Otherwise, nope, director exists already
    else:
        # Create a director instance using the schema and the passed in director
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the director to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_director)

        return Reponse(201,"Created Succesfully",[],data)
        

def update(id, director):
    """
    This function update a director from the director structure
    :param id:          Id of the director to update
    :body director:     Body of the director to update data
    :return:            200 on successful delete, 404 if not found, 409 body false
    """

    # Get the director requested from the db into session
    update_director = Director.query.filter(
        Director.id == id
    ).one_or_none()

    # Try to find an existing director with the same name as the update
    uid = director.get("uid")

    existing_director = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )

    # variable to check body with value not none
    validate_body = validator_body.director_required(director)    

    if validate_body[0]:
        return Reponse(409,validate_body[1],[],{})
    # Are we trying to find a director that does not exist?
    elif update_director is None:
        return Reponse(404,"Director not found for Id: {id}".format(id=id),[],{})

    # Would our update create a duplicate of another director already existing?
    elif (
        existing_director is not None and existing_director.id != id
    ):
        return Reponse(409,"Director {uid} exists already".format(uid=uid),[],{})

    # Otherwise go ahead and update!
    else:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return Reponse(200,"Update Successfully",[],data)


def delete(id):
    """
    This function deletes a director from the director structure
    :param id:          Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the director requested
    director = Director.query.filter(Director.id == id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return Reponse(200,"Director {id} deleted".format(id=id),[],{})

    # Otherwise, nope, didn't find that director
    else:
        return Reponse(200,"Director not found for Id: {id}".format(id=id).format(id=id),[],{})