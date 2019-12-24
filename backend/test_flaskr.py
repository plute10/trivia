import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    PER_PAGE = 10

    new_question = {
        'question': 'this is a test',
        'answer': 'Hi',
        'category': 1,
        'difficulty': 4
    }

    first_payload = {
        "previous_questions":[],
        "quiz_category":{"type":"Science","id":1}
    }

    second_payload = {
        "previous_questions":[5],
        "quiz_category":{"type":"Science","id":1}
    }

    search_test = {
        "search": 'test'
    }

    search_none = {
        "search": ""
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_having_questions_less_than_10(self):
        res1 = self.client().get('/questions')
        res2 = self.client().get('/questions?page=2')
        data1 = json.loads(res1.data)
        data2 = json.loads(res2.data)

        self.assertLessEqual(len(data1), self.PER_PAGE)
        self.assertLessEqual(len(data2), self.PER_PAGE)
        self.assertNotEqual(data1, data2)

    def test_having_the_same_questions(self):
        res1 = self.client().get('/questions')
        data_without_query = json.loads(res1.data)
        res2 = self.client().get('/questions?page=1')
        data_with_query = json.loads(res2.data)

        self.assertEqual(data_without_query, data_with_query)

    def test_deleting_one_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        id = data['questions'][0]['id']

        before_delete_total_num = data['total_questions']
        res = self.client().delete(F'/questions/{id}')
        data = json.loads(res.data)
        deleted_id = data['question_id']

        res = self.client().get('/questions')
        data = json.loads(res.data)
        after_delete_total_num = data['total_questions']

        self.assertEqual(id, deleted_id)
        self.assertEqual(before_delete_total_num - 1, after_delete_total_num)

    def test_deleting_non_existing_question(self):
        non_existing_id = 100000
        res = self.client().delete(F'/questions/{non_existing_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_posting_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_search(self):
        searchTerm = 'test'
        res = self.client().post(F'/questions', json=self.search_test)
        data = json.loads(res.data)

        self.assertTrue(searchTerm in data['questions'][0]['question'])

    def test_search_without_search_term(self):
        res = self.client().post(F'/questions', json=self.search_none)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable entity")

    def test_get_all_questions_based_on_category(self):
        category_id = 1
        res = self.client().get(F'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(data['total_questions'], 0)
        self.assertEqual(category_id, data['current_category'])

    def test_getting_a_random_question(self):
        res = self.client().post(F'/quizzes', json=self.first_payload)
        data = json.loads(res.data)

        self.assertTrue(data['question'])

        res = self.client().post(F'/quizzes', json=self.second_payload)
        data = json.loads(res.data)

        self.assertNotEqual(self.second_payload['previous_questions'][0], data['question']['id'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
