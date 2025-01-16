import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_module import Module as ModuleModel
from repositories.repository_course import RepositoryCourse
from repositories.repository_module import RepositoryModule
from schemas.common_shcema import Response
from schemas.module_schema import ModuleCreate, ModuleUpdate, OutputModulePage, Module as ModuleSchema
from sqlalchemy.orm import Session
from schemas.common_shcema import TokenData
from schemas.module_schema import ModuleCreate


class ServiceModule:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_module = RepositoryModule(session)
        self.repository_course = RepositoryCourse(session)

    def get_all(self, page: int, size: int, course_id: int):
        modules = self.repository_module.get_all(page, size, course_id)
        total_data = self.repository_module.count(course_id)
        total_page = math.ceil(total_data / size)

        return OutputModulePage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=modules
        ) 

    def insert(
        self, module_data: ModuleCreate, course_id: int
    ):
       course = self.repository_course.get_by_id(course_id)
       if not course:
            raise HTTPException(status_code=404, detail="Course not found")

       try:
           module = ModuleModel(
                course_id=course_id,
                title=module_data.title,
                description=module_data.description,
                sequence_number=module_data.sequence_number,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           self.repository_module.store_module(module, course_id)
           module = ModuleSchema.from_orm(module).dict()
           return Response(success=True, message="Module created", data=module)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def update( 
        self, module_data: ModuleUpdate, course_id: int, id: int
    ):
        module = self.repository_module.get_by_id_courseId(id, course_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        try:
            self.repository_module.update(id, course_id ,module_data)
            module = ModuleSchema.from_orm(module).dict()
            return Response(success=True, message="Module updated", data=module)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Internal server error")
        
    def delete(self, id: int, course_id: int):
        print()
        module = self.repository_module.get_by_id_courseId(id, course_id)
        if module is None:
            raise HTTPException(status_code=404, detail="Module not found")
        try:
            module = self.repository_module.delete(id, course_id)
            module = ModuleSchema.from_orm(module).dict()
            return Response(success=True, message="Module deleted", data=module)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Internal server error")
        
    