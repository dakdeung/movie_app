from app import connex_app
import unittest

class TestCase(unittest.TestCase):
    
    def test_get_all_movie(self):
        connex_app.app.test = True
        test = connex_app.app.test_client(self)
        response = test.get("/api/movie")
        self.assertEqual(response.status_code, 200)

    def test_get_all_director(self):
        connex_app.app.test = True
        test = connex_app.app.test_client(self)
        response = test.get("/api/director")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
