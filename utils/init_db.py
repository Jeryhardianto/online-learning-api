from config.config import Base, engine
from models.model_course import Course
from models.model_instructors import Instructor
from models.model_todo import Todo
from models.model_user import User


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Todo.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Course.metadata.create_all(bind=engine)
    Instructor.metadata.create_all(bind=engine)