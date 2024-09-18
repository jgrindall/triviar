import unittest
import json
from flaskr import create_app
from dotenv import load_dotenv
import os

load_dotenv()

PGPASSWORD = os.getenv("PGPASSWORD")

text_config = {
    "SQLALCHEMY_DATABASE_URI": 'postgresql://postgres:' + PGPASSWORD + '@localhost:5432/trivia_test'
}


class QuestionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(text_config)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions_page1(self):
        # default to page 1 if missing
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
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 0)


    def test_search_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm": "Which"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 7)
        self.assertTrue("Which" in data['questions'][0]['question'])

    def test_search_questions_invalid(self):

        res = self.client().post('/questions/search', json={"searchterm": "Which"})
        self.assertEqual(res.status_code, 422)

        res = self.client().post('/questions/search', json={})
        self.assertEqual(res.status_code, 422)




class CategoriesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(text_config)
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

    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['questions'][0]['category'], 1)

    def test_get_category_questions_nonexistant(self):
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


class QuizTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(text_config)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_quiz(self):
        previous_questions = []
        res = self.client().post('/quiz', json={
            "previous_questions": previous_questions, 
            "quiz_category_id": 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)

    def test_quiz_with_prev(self):
        previous_questions = [16, 17]

        for i in range(1000):

            res = self.client().post('/quiz', json={
                "previous_questions": previous_questions, 
                "quiz_category_id": 2
            })

            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertEqual(data['question']['category'], 2)
            self.assertIn(data['question']['id'], [18, 19])


    def test_quiz_missing_category_id(self):
        previous_questions = []
        res = self.client().post('/quiz', json={
            "previous_questions": previous_questions
        })
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_quiz_missing_category_id_with_prev(self):
        previous_questions = [2, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

        for i in range(1000):
            res = self.client().post('/quiz', json={
                "previous_questions": previous_questions
            })
            
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertIn(data['question']['id'], [21, 22, 23])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
