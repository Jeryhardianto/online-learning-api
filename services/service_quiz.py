import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_quiz import Quiz as QuizModel
from repositories.repository_module import RepositoryModule
from repositories.repository_quiz import RepositoryQuiz
from schemas.common_shcema import Response
from schemas.lesson_schema import LessonCreate, Lesson as LessonSchema, LessonUpdate, OutputLessonPage
from schemas.module_schema import ModuleCreate, ModuleUpdate, OutputModulePage, Module as ModuleSchema
from schemas.quiz_schema import QuizCreate, Quiz as QuizSchema, QuizUpdate, OutputQuizPage
from sqlalchemy.orm import Session
from schemas.common_shcema import TokenData
from schemas.module_schema import ModuleCreate
from schemas.quiz_schema import QuizCreate


class ServiceQuiz:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_quiz = RepositoryQuiz(session)
        self.repository_module = RepositoryModule(session)

    def get_all(self, page: int, size: int, module_id: int):
        quiz = self.repository_quiz.get_all(page, size, module_id)
        total_data = self.repository_quiz.count(module_id)
        total_page = math.ceil(total_data / size)

        return OutputQuizPage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=quiz
        )

    def insert(
        self, quiz_data: QuizCreate, module_id: int
    ):
       module = self.repository_module.get_by_id(module_id)
       if not module:
            raise HTTPException(status_code=404, detail="Module not found")

       try:
           quiz = QuizModel(
                module_id=module_id,
                title=quiz_data.title,
                passing_score=quiz_data.passing_score,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           quiz = self.repository_quiz.store(quiz, module_id)
           quiz = QuizSchema.from_orm(quiz).dict()
           return Response(success=True, message="Quiz created", data=quiz)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def update( 
        self,  quiz_data: QuizUpdate, module_id: int, id: int
    ):
        quiz = self.repository_quiz.get_by_id(module_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        try:
            quiz = self.repository_quiz.update(quiz_data, id)
            quiz = QuizSchema.from_orm(quiz).dict()
            return Response(success=True, message="Quiz updated", data=quiz)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Internal server error")
        
    def delete(self, id: int, module_id: int):
        quiz = self.repository_quiz.get_by_id(id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        try:
            quiz = self.repository_quiz.delete(id)
            quiz = QuizSchema.from_orm(quiz).dict()
            return Response(success=True, message="Quiz deleted", data=quiz)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Internal server error")