from app import connex_app
import unittest

class TestCase(unittest.TestCase):
    """
    This class for testing function
    """
    def test_get_all_movie(self):
        """
        This function for testing get all movie
        """
        connex_app.app.test = True
        test = connex_app.app.test_client(self)
        response = test.get("/api/movie")
        self.assertEqual(response.status_code, 200)

    def test_get_all_director(self):
        """
        This function for testing get all director
        """
        connex_app.app.test = True
        test = connex_app.app.test_client(self)
        response = test.get("/api/director")
        self.assertEqual(response.status_code, 200)

    def test_get_all_genre(self):
        """
        This function for testing get all genre
        """
        connex_app.app.test = True
        test = connex_app.app.test_client(self)
        response = test.get("/api/genre")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
