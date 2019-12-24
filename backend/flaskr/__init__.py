import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Category, Question, db
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    PER_PAGE = 10

    def change_category(categories):
        dict_categories = {}
        for one in categories:
            dict_categories[one.id] = one.type
        return dict_categories

    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * PER_PAGE
        end = start + PER_PAGE

        fotmatted_selection = [one.format() for one in selection]
        return fotmatted_selection[start:end]

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST,' +
                             'PATCH, DELETE, OPTIONS')
        return response

    # GET: return all categories
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': change_category(categories)
        })

    # GET: return all questions
    @app.route('/questions')
    def get_all_questions():
        questions = Question.query.all()
        categories = Category.query.all()

        if len(questions) == 0 or len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginate(request, questions),
            'total_questions': len(questions),
            'currentCategory': None,
            'categories': change_category(categories)
        })

    # DELETE: delete one question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            Question.query.filter_by(id=question_id).delete()
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        return jsonify({
            'success': True,
            'question_id': question_id
        })

    # POST: post new question
    # details of the question are required
    # POST: when the request has body
    # it returns the questions having searchTerm
    @app.route('/questions', methods=['POST'])
    def post_new_question():
        search = request.get_json().get('search')
        if search != None:
            return search_questions(search)
        try:
            body = request.get_json()
            new_question = Question(
                question=body.get('question'),
                answer=body.get('answer'),
                category=body.get('category'),
                difficulty=body.get('difficulty')
            )
            db.session.add(new_question)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        return jsonify({
            'success': True
        })

    # POST: it returns the questions having searchTerm
    def search_questions(searchTerm):
        if searchTerm == '':
            abort(422)
        searchTerm = F'%{searchTerm}%'
        questions = (Question.query
                     .filter(Question.question.like(searchTerm))
                     .all())
        return jsonify({
            'success': True,
            'questions': [one.format() for one in questions],
            'total_questions': len(questions),
            'current_category': 1
        })

    # GET: get all questions based on category id
    @app.route('/categories/<int:category_id>/questions')
    def get_all_questions_based_on_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()

        return jsonify({
            'success': True,
            'questions': [one.format() for one in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })

    # POST: return a random question
    # which is not the same with the previous question
    @app.route('/quizzes', methods=['POST'])
    def get_a_random_question():
        body = request.get_json()
        prev = body.get('previous_questions')
        category = body.get('quiz_category')['id']
        if category == 0:
            if len(prev) > 0:
                question = (Question.query
                            .filter(Question.id != prev[len(prev) - 1])
                            .first())
            else:
                question = Question.query.first()
        else:
            if len(prev) > 0:
                question = (Question.query
                            .filter(Question.id != prev[len(prev) - 1])
                            .filter_by(category=category)
                            .first())
            else:
                question = Question.query.filter_by(category=category).first()

        if question is None:
            abort(404)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
            }), 422

    return app
