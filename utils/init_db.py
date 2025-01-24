from config.config import Base, engine
from models.model_course import Course
from models.model_instructors import Instructor
from models.model_todo import Todo
from models.model_user import User
from models.model_enroll import Enrollment
from models.model_module import Module
from models.model_lesson import Lesson
from models.model_quiz import Quiz
from models.model_question import Question
from models.model_answre import Answre


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Todo.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Course.metadata.create_all(bind=engine)
    Instructor.metadata.create_all(bind=engine)
    Enrollment.metadata.create_all(bind=engine)
    Module.metadata.create_all(bind=engine)
    Lesson.metadata.create_all(bind=engine)
    Quiz.metadata.create_all(bind=engine)
    Question.metadata.create_all(bind=engine)
    Answre.metadata.create_all(bind=engine)

    