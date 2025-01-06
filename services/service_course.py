import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_course import Course as CourseModel
from repositories.repository_course import RepositoryCourse
from schemas.common_shcema import Response, TokenData
from schemas.course_schema import OutputCoursePage, Course as CourseSchema, CourseCreate, CourseUpdate, CourseImage
from sqlalchemy.orm import Session
import os
from pathlib import Path

from utils.format_file_upload import format_file_upload
from utils.validation_image import validate_file_type


class ServiceCourse:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_course = RepositoryCourse(session)
    
    def get_list_course(self, page: int, size: int):
        skip = page * size
        total_data = self.repository_course.count()
        courses = self.repository_course.get_all(skip, size)
        total_page = math.ceil(total_data / size)

        result = OutputCoursePage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=courses
        )
        return result
    
    
    def get_by_id(self, id: int):
        course = self.repository_course.get_by_id(id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        # create course to dict
        course = CourseSchema.from_orm(course).dict()
        return Response(success=True, message="Course found", data=course)
    
    def insert(
        self, course_data: CourseCreate
    ):
       try:
           course = CourseModel(
                title=course_data.title,
                description=course_data.description,
                instructor_id=course_data.instructor_id,
                price=course_data.price,
                difiiculty=course_data.difiiculty,
                is_published=course_data.is_published,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           courseId = self.repository_course.store_course(course)
           course = CourseSchema.from_orm(course).dict()
           course["course_id"] = courseId    
           return Response(success=True, message="Course created", data=course)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
       
    def update(self, id: int, course_data: CourseUpdate):
        found_course = self.repository_course.get_by_id(id)
        if found_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        
        try:
            course = self.repository_course.update(id, course_data)
            course = CourseSchema.from_orm(course).dict()
            return Response(success=True, message="Course updated", data=course)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def upload_image(self, id: int, file):

        found_course = self.repository_course.get_by_id(id)
        if found_course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        # Define allowed file types
        allowed_types = ["image/jpeg", "image/png", "image/gif"]

        try:
            # Validate file type
            validate_file_type(file, allowed_types)
            
            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            file_size = 0

            COURSES_DIR = Path("uploads/courses")
            COURSES_DIR.mkdir(exist_ok=True)

            file_path = COURSES_DIR / format_file_upload(file.filename)
            with file_path.open("wb") as buffer:
                while chunk := file.file.read(8192):  # Read in chunks
                    file_size += len(chunk)
                    if file_size > max_size:
                        buffer.close()
                        os.unlink(file_path)  # Delete partially uploaded file
                        raise HTTPException(
                            status_code=400,
                            detail="File size exceeds maximum limit of 5MB"
                        )
                    buffer.write(chunk)
            course = self.repository_course.upload_image_by_id(id, file_path)
            course = CourseImage.from_orm(course).dict()
            return Response(success=True, message="Image created", data=course)
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
        finally:
            file.file.close()

    def delete(self, id: int):
        found_course = self.repository_course.get_by_id(id)
        if found_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        try:
            course = self.repository_course.delete(id)
            course = CourseSchema.from_orm(course).dict()
            return Response(success=True, message="Course deleted", data=course)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))