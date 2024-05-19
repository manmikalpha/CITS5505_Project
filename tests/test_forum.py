import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from app import db

class ForumTest(TestCase):

    def create_app(self):
        # Configure the app for testing
        app.config.from_object('test_config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_forum_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Public Forum', response.data)

    def test_add_question(self):
        response = self.client.post('/add_question', json={'text': 'What is your name?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'What is your name?', response.data)
        question = Question.query.first()
        self.assertIsNotNone(question)
        self.assertEqual(question.text, 'What is your name?')

    def test_add_answer(self):
        # Add a question first
        question = Question(text='What is your name?')
        db.session.add(question)
        db.session.commit()

        # Add an answer to the question
        response = self.client.post('/add_answer', json={'text': 'My name is Mihir', 'question_id': question.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My name is Mihir', response.data)
        answer = Answer.query.first()
        self.assertIsNotNone(answer)
        self.assertEqual(answer.text, 'My name is Mihir')
        self.assertEqual(answer.question_id, question.id)

if __name__ == '__main__':
    unittest.main()
