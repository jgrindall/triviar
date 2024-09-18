from .questions import setup as setup_questions
from .categories import setup as setup_categories
from .quiz import setup as setup_quiz
from .errors import setup as setup_errors


def init_routes(app):
    # Register all routes
    setup_questions(app)
    setup_categories(app)
    setup_quiz(app)
    setup_errors(app)
