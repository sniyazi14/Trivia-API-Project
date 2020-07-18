import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, list):
    page = request.args.get('page', 1, type=int)
    begin = (page - 1) * QUESTIONS_PER_PAGE
    end = begin + QUESTIONS_PER_PAGE
    questions = []
    count = 0
    for question in list:
        count = count + 1
        if count > begin and count <= end:
            questions.append(question.format())
    return questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Fetch all categories
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.all()
        format_categories = {category.id: category.type
                             for category in categories}
        result = {
            "success": True,
            "categories": format_categories
        }
        return jsonify(result)

    # Fetches questions with pagination,
    # page number specified with query parameter 'page'
    @app.route('/questions')
    def retrieve_books():
        categories = Category.query.all()
        formated_categories = {category.id: category.type
                               for category in categories}
        data = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, data)
        if len(questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': questions,
            'categories': formated_categories,
            'currentCategory': 1,
            'totalQuestions': len(Question.query.all())
        })

    # Delete a specified question from the database
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            data = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, data)
            categories = Category.query.all()
            category = {category.id: category.type
                        for category in categories}
            return jsonify({
                'success': True,
                'questions': current_questions,
                'categories': category,
                'currentCategory': 1,
                'totalQuestions': len(Question.query.all())
            })
        except Exception:
            abort(422)

    # Create a new question in the database
    @app.route('/questions/add', methods=['POST'])
    def add_question():
        try:
            question = request.json.get('question', '')
            answer = request.json.get('answer', '')
            category = request.json.get('category', '')
            difficulty = request.json.get('difficulty', '')
            new_question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
            new_question.insert()
            return jsonify({
              'success': True
            })
        except Exception:
            abort(422)

    # Search for a question that contains a specified substring
    @app.route('/questions/search', methods=['POST'])
    def search_4_question():
        search_term = request.json.get('searchTerm', '')
        try:
            data = Question.query.filter(Question.question.ilike('%{}%'
                                         .format(search_term))).all()
            questions = paginate_questions(request, data)
            return jsonify({
              'success': True,
              'questions': questions,
              'totalQuestions': len(questions),
              'currentCategory': 1
            })
        except Exception:
            abort(422)

    # Fetch all questions from a specified category using pagination
    @app.route('/categories/<int:cat_id>/questions')
    def get_question_by_cat(cat_id):
        category = Category.query.get(cat_id)
        if not category:
            abort(404)
        data = Question.query.filter(Question.category == category.id).all()
        questions = paginate_questions(request, data)
        return jsonify({
          'success': True,
          'questions': questions,
          'currentCategory': cat_id,
          'totalQuestions': len(data)
        })

    # Fetch a question while playing a quiz
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            body = request.get_json()
            category_id = int(body["quiz_category"]["id"])
            category = Category.query.get(category_id)
            previous_questions = body["previous_questions"]
            if category is None:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category
                                                  == str(category.id)).all()
            if questions is None:
                abort(422)
            quiz_questions = []
            for q in questions:
                if q.id not in previous_questions:
                    quiz_questions.append(q)
            if len(quiz_questions) > 0:
                index = random.randint(0, len(quiz_questions) - 1)
                question = quiz_questions[index].format()
                return jsonify({
                    "success": True,
                    "question": question
                })
            else:
                return jsonify({
                  "success": False,
                  "question": False
                })
        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable entity"
        }), 422

    return app
