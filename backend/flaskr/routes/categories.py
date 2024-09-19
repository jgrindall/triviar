"""
Categories controller
"""

from flask import abort, jsonify
from models import Category, db
from werkzeug.exceptions import HTTPException


def _abort(e):
    if isinstance(e, HTTPException):
        abort(e.code)
    else:
        abort(500)


def setup(app):
    """
    An endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.all()
            categories_formatted = [cat.format() for cat in categories]
            categories_hash = {
                cat["id"]: cat["type"] for cat in categories_formatted
            }

            return jsonify({
                "success": True,
                "categories": categories_hash
            })

        except Exception as e:
            _abort(e)

    """
    A GET endpoint to get questions based on category.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_for_category(category_id):
        try:
            category = db.session.get(Category, category_id)

            if category is None:
                abort(404)
            else:
                questions_formatted = [q.format() for q in category.questions]

                return jsonify({
                    "success": True,
                    "questions": questions_formatted
                })

        except Exception as e:
            _abort(e)
