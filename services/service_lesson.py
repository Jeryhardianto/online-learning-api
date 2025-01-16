import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_module import Module as ModuleModel
from models.model_lesson import Lesson as LessonModel
from repositories.repository_course import RepositoryCourse
from repositories.repository_lesson import RepositoryLesson
from repositories.repository_module import RepositoryModule
from schemas.common_shcema import Response
from schemas.lesson_schema import LessonCreate, Lesson as LessonSchema, LessonUpdate, OutputLessonPage
from schemas.module_schema import ModuleCreate, ModuleUpdate, OutputModulePage, Module as ModuleSchema
from sqlalchemy.orm import Session
from schemas.common_shcema import TokenData
from schemas.module_schema import ModuleCreate


class ServiceLesson:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_lesson = RepositoryLesson(session)
        self.repository_module = RepositoryModule(session)

    def get_all(self, page: int, size: int, module_id: int):
        lesson = self.repository_lesson.get_all(page, size, module_id)
        total_data = self.repository_lesson.count(module_id)
        total_page = math.ceil(total_data / size)

        return OutputLessonPage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=lesson
        )

    def insert(
        self, lesson_data: LessonCreate, module_id: int
    ):
       module = self.repository_module.get_by_id(module_id)
       if not module:
            raise HTTPException(status_code=404, detail="Module not found")

       try:
           lesson = LessonModel(
                module_id=module_id,
                title=lesson_data.title,
                content=lesson_data.content,
                video_url=lesson_data.video_url,
                duration_minutes=lesson_data.duration_minutes,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           lesson = self.repository_lesson.store_lesson(lesson, module_id)
           lesson = LessonSchema.from_orm(lesson).dict()
           return Response(success=True, message="Lesson created", data=lesson)   
       except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Internal server error")
    
    def update( 
        self, lesson_data: LessonUpdate, module_id: int, id: int
    ):
        module = self.repository_module.get_by_id(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        try:
            lesson = self.repository_lesson.update(id, module_id ,lesson_data)
            lesson = LessonSchema.from_orm(lesson).dict()
            return Response(success=True, message="Module updated", data=lesson)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Internal server error")
        
    # def delete(self, id: int, course_id: int):
    #     print()
    #     module = self.repository_module.get_by_id(id, course_id)
    #     if module is None:
    #         raise HTTPException(status_code=404, detail="Module not found")
    #     try:
    #         module = self.repository_module.delete(id, course_id)
    #         module = ModuleSchema.from_orm(module).dict()
    #         return Response(success=True, message="Module deleted", data=module)
    #     except Exception as e:
    #         print(e)
    #         raise HTTPException(status_code=400, detail="Internal server error")
        
    