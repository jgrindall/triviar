"""
Questions controller
"""

from flask import request, abort
from flask import jsonify
from models import Question, Category, db
from werkzeug.exceptions import HTTPException


QUESTIONS_PER_PAGE = 10

def _abort(e):
    if isinstance(e, HTTPException):
        abort(e.code)
    else:
        abort(500)


def setup(app):

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            page = request.args.get("page", 1, type=int)
            offset = (page - 1) * QUESTIONS_PER_PAGE

            query = (
                Question.query
                .offset(offset)
                .limit(QUESTIONS_PER_PAGE)
            )

            questions = query.all()
            questions_formatted = [ques.format() for ques in questions]

            categories = Category.query.all()
            categories_formatted = [cat.format() for cat in categories]

            # client expects a hash of categories
            categories_hash = {
                cat["id"]: cat["type"] for cat in categories_formatted
            }

            return jsonify({
                "success": True,
                "questions": questions_formatted,
                "categories": categories_hash,
                "total_questions": Question.query.count()
            })

        except Exception as e:
            print(e, flush=True)
            _abort(e)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a
    question, the question will be removed.
    This removal will persist in the database
    and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        print("delete_question", flush=True)
        try:

            question = (
                Question.query
                .filter(Question.id == question_id)
                .one_or_none()
            )

            if question is None:
                abort(404)

            else:
                question.delete()

                return jsonify({
                    "success": True
                })

        except Exception as e:
            db.session.rollback()
            print(e, flush=True)
            _abort(e)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        print("create_question", flush=True)
        try:
            data = request.get_json()
            new_question = Question.get_validated_question(data)

            if not new_question:
                abort(422)

            else:
                new_question.insert()
                return jsonify({
                    "success": True
                })

        except Exception as e:
            print(e, flush=True)
            db.session.rollback()
            _abort(e)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            data = request.get_json()

            if "searchTerm" not in data or not data["searchTerm"]:
                abort(422)

            else:
                search_term = data["searchTerm"].strip()
                search_term_wildcard = "%" + search_term + "%"

                questions = (
                    Question.query
                    .filter(Question.question.ilike(search_term_wildcard))
                    .all()
                )

                formatted_questions = [q.format() for q in questions]

                return jsonify({
                    "success": True,
                    "questions": formatted_questions
                })

        except Exception as e:
            print(e, flush=True)
            _abort(e)
