import unittest
import json
from flaskr import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": 'postgresql://postgres:thisismypassword@localhost:5432/trivia_test'
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    
    def test_get_paginated_questions_page1(self):
        # default to page 1
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 19)
        # the first page should have 10 questions
        self.assertTrue(len(data['questions']), 10)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['categories']["1"], "Science")
        
    
    def test_get_paginated_questions_page2(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 19)
        # the second page should have 9 questions
        self.assertTrue(len(data['questions']), 9)

        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['categories']["1"], "Science")


    def test_get_paginated_questions_page_nonexistant(self):
        res = self.client().get('/questions?page=2000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
        

    def test_search_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm": "Which"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 7)
        self.assertTrue("Which" in data['questions'][0]['question'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()