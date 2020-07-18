import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:1234@localhost:5432/trivia_test'#"postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
            'question':'New question',
            'answer':'New answer',
            'category':1,
            'difficulty':5
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['currentCategory'], 1)
        self.assertTrue(data['totalQuestions'])

    def test_get_questions_by_nonexist_category(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_404_nonexist_questions_page(self):
        res = self.client().get('/questions?page=250')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_question_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(len(data['questions']), 2)

    def test_questions_search_none_found(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'ja'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_get_quiz_question(self):
        res = self.client().post('/quizzes', json={'previous_questions': [16],'quiz_category': {'type':'Art','id': '2'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_quiz_no_question(self):
        res = self.client().post('/quizzes', json={'previous_questions': [10,11],'quiz_category': {'type':'Sports','id': '6'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['question'], False)

    def test_add_question(self):
        res = self.client().post('/questions/add', json=self.question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_question_without_data(self):
        res = self.client().post('/questions/add')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')


    def test_delete_book(self):
        res = self.client().delete('/questions/16')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 16).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertEqual(question, None)

    def test_delete_nonexistent_book(self):
        res = self.client().delete('/questions/666')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
