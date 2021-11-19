from models import Movie, Genre

class validator_body():
    """
    This class for validator function
    """
    def movie_required(movie):
        """
        This function for validator from movie
        """
        data = [False,""]
        if movie.get("original_title") is None:
            data = [True,"Original Title cannot be null"]
            return data
        elif movie.get("budget") is None:
            data = [True,"Budget cannot be null"]
            return data
        elif movie.get("popularity") is None:
            data = [True,"Popularity cannot be null"]
            return data
        elif movie.get("release_date") is None:
            data = [True,"Release Date cannot be null"]
            return data
        elif movie.get("revenue") is None:
            data = [True,"Revenue cannot be null"]
            return data
        elif movie.get("title") is None:
            data = [True,"Title cannot be null"]
            return data
        elif movie.get("vote_average") is None:
            data = [True,"Vote Average cannot be null"]
            return data
        elif movie.get("vote_count") is None:
            data = [True,"Vote Count cannot be null"]
            return data
        elif movie.get("overview") is None:
            data = [True,"Overview cannot be null"]
            return data
        elif movie.get("tagline") is None:
            data = [True,"Tagline cannot be null"]
            return data
        elif movie.get("uid") is None:
            data = [True,"Uid cannot be null"]
            return data
        elif movie.get("director_id") is None:
            data = [True,"Director_id cannot be null"]
            return data
        elif movie.get("genre") is None:
            data = [True,"Genre cannot be null"]
            return data
        elif type(movie.get("genre")[0]) is dict:
            data = [True,"Genre cannot be dict"]
            return data
        return data
    
    def director_required(director):
        """
        This function for validator from director
        """
        data = [False, ""]

        if director.get("name") is None:
            data = [True,"Name cannot be null"]
            return data
        elif director.get("gender") is None:
            data = [True,"Gender cannot be null"]
            return data
        elif director.get("uid") is None:
            data = [True,"Uid cannot be null"]
            return data
        elif director.get("department") is None:
            data = [True,"Department cannot be null"]
            return data
        return data

    def genre_required(genre):
        """
        This function for validator from genre
        """
        data = [False, ""]

        if genre.get("name") is None:
            data = [True,"Name cannot be null"]
            return data
        elif genre.get("movie") is None or genre.get("movie") == False:
            data = [True,"Movie cannot be null"]
            return data
        elif type(genre.get("movie")[0]) is dict:
            data = [True,"Movie cannot be dict"]
            return data
        return data

    def check_date(start,end):
        """
        This function for validator date format
        """
        if len(start) < 9 and len(end) <9:
            return True
        else:
            if start[4] != "-" and start[7] != "-": 
                check_start = True
            else:
                check_start = False

            if end is not None:
                if end[4] != "-" and end[7] != "-": 
                    check_end = True
            else:
                check_end = False
        
        if check_start and check_end:
            return True
        else:
            return False
    
    def check_genre_value(movie):
        """
        This function for validator value from array genre
        """
        data = [True,""]
        genre = movie.get("genre")
        # check genre value

        if genre is not None:   
            count = 0
            for x in genre:
                name_genre = Genre.query.filter(Genre.id == x).one_or_none()
                if name_genre is None:
                    data = [True, x]
                else:
                    count += 1
            if count == len(genre):
                data = [False, ""]
        return data


    def check_movie_value(genre):
        """
        This function for validator value from array movie
        """
        data = [True,""]
        movie = genre.get("movie")
        # check genre value

        if movie is not None:   
            count = 0
            for x in movie:
                name_movie = Movie.query.filter(Movie.id == x).one_or_none()
                if name_movie is None:
                    data = [True, x]
                else:
                    print(count)
                    count += 1
            if count == len(movie):
                data = [False, ""]
        return data
      
                
        