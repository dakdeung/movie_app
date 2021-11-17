from config import db, ma
from marshmallow import fields
from sqlalchemy.orm import backref
from marshmallow import EXCLUDE

movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
)

class Movie(db.Model):
    __tablename__ = 'movies'
    title = db.Column(db.String(1000))
    budget = db.Column(db.Integer)
    original_title = db.Column(db.String(1000))
    overview = db.Column(db.String(1000))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    release_date = db.Column(db.String(50))
    popularity = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    tagline = db.Column(db.String(1000))
    uid = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.Float)
    directors = db.relationship('Director', backref=backref("movies"))
    genres = db.relationship('Genre',
                               secondary=movie_genre, back_populates="movies")

class Director(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String(50))

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    movies = db.relationship("Movie",
        secondary=movie_genre,
        back_populates="genres")

class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    directors = fields.Nested('MovieDirectorSchema', default=[])
    genres = fields.Nested('MovieGenreSchema', default=[], many=True)

class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name = fields.Str() 
    id = fields.Int()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()

class MovieGenreSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

    id = fields.Int()
    name = fields.Str()

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    movies = fields.Nested("DirectorMovieSchema", default=[], many=True)


class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int() 
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()

class GenreSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Genre
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    movies = fields.Nested("GenreMovieSchema", default=[], many=True)


class GenreMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int() 
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()