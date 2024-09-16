from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy

default_uri = 'postgresql://postgres:thisismypassword@localhost:5432/trivia'

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path = default_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    app.app_context().push()
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, unique=True, nullable=False)
    answer = Column(String, unique=True, nullable=False)
    difficulty = Column(Integer, nullable=False)
    category = db.Column(db.Integer, ForeignKey('categories.id', ondelete='SET NULL', onupdate='CASCADE'))
    matching_category = db.relationship('Category', backref = db.backref('questions', cascade="all, delete-orphan", lazy=True))

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


    """
    validate_question(data)
        
    """
    @staticmethod
    def get_validated_question(data):
        if "question" not in data or "answer" not in data or "category" not in data or "difficulty" not in data:
            return None
        question = data["question"].strip()
        answer = data["answer"].strip()
        category = int(data["category"])
        difficulty = int(data["difficulty"])
        if not question or not answer or not category or not difficulty:
            return None
        
        return Question(question=question, answer=answer, category=category, difficulty=difficulty)





"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, unique=True, nullable=False)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }


