import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_instructors import Instructor as InstructorModel
from repositories.repository_instructor import RepositoryInstructor
from schemas.common_shcema import Response
from schemas.instructor_schema import InsructorCreate, Insructor as InsructorSchema, OutputInsructorPage, InsructorUpdate
from sqlalchemy.orm import Session

from utils.format_file_upload import format_file_upload
from utils.validation_image import validate_file_type


class ServiceInstructor:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_instructor = RepositoryInstructor(session)
    
    def get_list_instructor(self, page: int, size: int):
        skip = page * size
        total_data = self.repository_instructor.count()
        instructor = self.repository_instructor.get_all(skip, size)
        total_page = math.ceil(total_data / size)

        result = OutputInsructorPage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=instructor
        )
        return result
    
    
    def get_by_id(self, id: int):
        instructor = self.repository_instructor.get_by_id(id)
        if instructor is None:
            raise HTTPException(status_code=404, detail="Instructor not found")
        # create course to dict
        instructor = InsructorSchema.from_orm(instructor).dict()
        return Response(success=True, message="Instructor found", data=instructor)
    
    def insert(
        self, instructor_data: InsructorCreate
    ):
       email_is_exist = self.repository_instructor.get_by_email(instructor_data.email)
       if email_is_exist:
          raise HTTPException(status_code=400, detail="Email already exist")

       try:
           instructor = InstructorModel(
                first_name=instructor_data.first_name,
                last_name=instructor_data.last_name,
                email=instructor_data.email,
                bio=instructor_data.bio,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           self.repository_instructor.store_instructor(instructor)
           instructor = InsructorSchema.from_orm(instructor).dict()
           return Response(success=True, message="Instructor created", data=instructor)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
       
    def update(self, id: int, instructor_data: InsructorUpdate):
        found_instructor = self.repository_instructor.get_by_id(id)
        if found_instructor is None:
            raise HTTPException(status_code=404, detail="Instructor not found")
        
        try:
            instructor = self.repository_instructor.update(id, instructor_data)
            instructor = InsructorSchema.from_orm(instructor).dict()
            return Response(success=True, message="Instructor updated", data=instructor)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
      
    def delete(self, id: int):
        found_instructor = self.repository_instructor.get_by_id(id)
        if found_instructor is None:
            raise HTTPException(status_code=404, detail="Instructor not found")
        try:
            instructor = self.repository_instructor.delete(id)
            instructor = InsructorSchema.from_orm(instructor).dict()
            return Response(success=True, message="Instructor deleted", data=instructor)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))