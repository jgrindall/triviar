"""
Quiz controller
"""

from flask import request, abort
from flask import jsonify
from sqlalchemy import func
from models import Question
from werkzeug.exceptions import HTTPException


def _abort(e):
    if isinstance(e, HTTPException):
        abort(e.code)
    else:
        abort(500)


def setup(app):
    """
    A POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random question within the given category,
    if provided, and that is not one of the previous questions.
    """

    @app.route("/quiz", methods=["POST"])
    def get_quiz_question():
        data = request.get_json()
        try:
            # array of ids
            previous_questions = data.get("previous_questions", None)
            # optional, can be None
            quiz_category_id = data.get("quiz_category_id", None)

            query = Question.query

            if previous_questions is not None and isinstance(previous_questions, list) and len(previous_questions) >= 1:
                query = query.filter(Question.id.notin_(previous_questions))

            if quiz_category_id is not None:
                query = query.filter(Question.category == quiz_category_id)

            query = query.order_by(func.random())
            question = query.first()

            if question is None:
                #perhaps we have done all the questions. This is a success
                return jsonify({
                    "success": True,
                    "question": None
                })

            else:
                return jsonify({
                    "success": True,
                    "question": question.format()
                })

        except Exception as e:
            print(e, flush=True)
            _abort(e)
