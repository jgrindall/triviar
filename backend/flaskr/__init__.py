from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask("flaskr")

    if test_config is None:
        setup_db(app)
    else:
        setup_db(app, database_path=test_config.get('SQLALCHEMY_DATABASE_URI'))

    
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """


    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    



    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=["GET"])
    def get_categories():
        print("get_categories", flush=True)
        try:
            categories = Category.query.all()
            categories_formatted = [cat.format() for cat in categories]

            return jsonify({
                "success": True,
                "categories": categories_formatted
            })
        
        except Exception as e:
            print(e, flush=True)
            abort(500)



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        print("get_questions", flush=True)
        
        try:
            page = request.args.get("page", 1, type = int)
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

            #client expects a hash of categories
            categories_hash = {cat["id"]: cat["type"] for cat in categories_formatted}

            return jsonify({
                "success": True,
                "questions": questions_formatted,
                "categories": categories_hash,
                "total_questions": Question.query.count()
            })
        
        except Exception as e:
            print(e, flush=True)
            abort(500)

   

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
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
            abort(500)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
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
            db.session.rollback()
            print(e, flush=True)
            abort(500)




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
        print("search_questions", flush=True)
        try:
            data = request.get_json()

            if "searchTerm" not in data:
                abort(400)
            
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
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_for_category(category_id):
        print("get_categories", flush=True)
        try:

            questions = (
                Question.query
                .filter(Question.category == category_id)
                .all()
            )
            
            questions_formatted = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": questions_formatted
            })
        
        except Exception as e:
            print(e, flush=True)
            abort(500)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        print("get_quiz_question", flush=True)
        pass




    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        })
        return (json, 404)
    

    @app.errorhandler(422)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 422,
            "message": "Badly formatted request"
        })
        return (json, 422)
    

    @app.errorhandler(500)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        })
        return (json, 500)

   
    '''

    @app.route("/books/<int:book_id>")
    def get_book(book_id):
        b = Book.query.filter(Book.id == book_id).one_or_none()
        if b is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "book": b.format()
            })


    @app.route("/books/<int:book_id>/rate", methods=["PATCH"])
    def update_book(book_id):
        data = request.get_json()
        b = Book.query.filter(Book.id == book_id).one_or_none()
        if b is None:
            abort(404)
        else:
            b.rating = int(data["rating"])
            b.update()
            return jsonify({
                "success": True
            })


    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        b = Book.query.filter(Book.id == book_id).one_or_none()
        if b is None:
            abort(404)
        else:
            b.delete()
            total_books = Book.query.count()
            return jsonify({
                "success": True,
                "deleted": book_id,
                "total_books": total_books
            })

    
    @app.route("/books", methods=["POST"])
    def create_book():
        try:
            data = request.get_json()
            b = Book(title=data["title"], author=data["author"], rating=data["rating"])
            b.insert()

            total_books = Book.query.count()
            return jsonify({
                "success": True,
                "created": b.id,
                "total_books": total_books
            })
        except Exception as e:
            db.session.rollback()
            print(e, flush=True)
            abort(500)
    

    @app.route("/books/search", methods=["POST"])
    def search_books():
        try:
            data = request.get_json()
            search_term = data["search"]
            search_term_wildcard = "%" + search_term + "%"
            books = Book.query.filter(Book.title.ilike(search_term_wildcard)).all()
            formatted = [b.format() for b in books]
            return jsonify({
                "success": True,
                "books": formatted
            })
        except Exception as e:
            db.session.rollback()
            print(e, flush=True)
            abort(500)

    @app.errorhandler(404)
    def not_found_error(error):
        json = jsonify({
            "success": False,
            "error": 404,
            "message": "2 Book not found!!"
        })
        return (json, 404)

    '''

    return app

