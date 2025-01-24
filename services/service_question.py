import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from models.model_question import Question as QuestionModel
from repositories.repository_module import RepositoryModule
from repositories.repository_question import RepositoryQuestion
from repositories.repository_quiz import RepositoryQuiz
from schemas.common_shcema import Response
from schemas.question_schema import OutputQuestionPage, QuestionCreate, Question as QuestionSchema, QuestionUpdate
from sqlalchemy.orm import Session
from schemas.common_shcema import TokenData
from schemas.module_schema import ModuleCreate
from schemas.quiz_schema import QuizCreate


class ServiceQuestion:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_quiz = RepositoryQuiz(session)
        self.repository_question = RepositoryQuestion(session)

    def get_all(self, page: int, size: int, quiz_id: int):
        question = self.repository_question.get_all(page, size, quiz_id)
        total_data = self.repository_question.count(quiz_id)
        total_page = math.ceil(total_data / size)

        return OutputQuestionPage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=question
        )

    def insert(
        self, question_data: QuestionCreate, quiz_id: int
    ):
       quiz = self.repository_quiz.get_by_id(quiz_id)
       if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
       try:
           question = QuestionModel(
                quiz_id=quiz_id,
                question=question_data.question,
                point=question_data.point,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           question = self.repository_question.store(question, quiz_id)
           question = QuestionSchema.from_orm(question).dict()
           return Response(success=True, message="Question created", data=question)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    def update(self, question_data: QuestionUpdate, id: int):
        question = self.repository_question.get_by_id(id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            question = self.repository_question.update(question_data, id)
            question = QuestionSchema.from_orm(question).dict()
            return Response(success=True, message="Question updated", data=question)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Internal server error")
   
    def delete(self, id: int):
        question = self.repository_question.get_by_id(id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            question = self.repository_question.delete(id)
            question = QuestionSchema.from_orm(question).dict()
            return Response(success=True, message="Question deleted", data=question)
        except Exception as e:

            raise HTTPException(status_code=400, detail=str(e))