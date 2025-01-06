import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException
from config.config import UPLOAD_DIR
from models.model_enroll import Enrollment as EnrollmentModel
from repositories.repository_enroll import RepositoryEnroll
from schemas.common_shcema import Response
from schemas.enroll_schema import EnrollComplate, EnrollCreate, OutputEnrollPage, Enroll as EnrollSchema
from sqlalchemy.orm import Session
from schemas.common_shcema import TokenData


class ServiceEnrroll:
    def __init__(
        self, session: Session,
    ) -> None:
        self.repository_enroll = RepositoryEnroll(session)
    
    def get_list_enroll(self, page: int, size: int, current_user: TokenData):
        match_filter = {"user_id": current_user.id}
        skip = page * size
        total_data = self.repository_enroll.count(match_filter)
        enroll = self.repository_enroll.get_all(skip, size, match_filter)
        total_page = math.ceil(total_data / size)

        result = OutputEnrollPage(
            total_data=total_data,
            total_page=total_page,
            page=page,
            size=size,
            data=enroll
        )
        return result

    def insert(
        self, enroll_data: EnrollCreate, current_user: TokenData
    ):
       user_id = current_user.id
       course_is_enroll = self.repository_enroll.check_course_is_enroll(user_id, enroll_data.course_id)
       if course_is_enroll:
          raise HTTPException(status_code=400, detail="Course already enroll")

       try:
           enroll = EnrollmentModel(
                user_id=user_id,
                course_id=enroll_data.course_id,
                enrolled_date=enroll_data.enrolled_date,
                status=enroll_data.status,
                created_at=datetime.now(),
                updated_at=datetime.now()
           )
           self.repository_enroll.store_enroll(enroll, user_id)
           enroll = EnrollSchema.from_orm(enroll).dict()
           return Response(success=True, message="Enrollment created", data=enroll)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def complate(
        self, course_id, enroll_data: EnrollComplate, current_user: TokenData
    ):
       user_id = current_user.id
       course_is_enroll = self.repository_enroll.check_course_is_enroll(user_id, course_id)
       if not course_is_enroll:
          raise HTTPException(status_code=400, detail="Course not enroll")

       try:
           self.repository_enroll.update_enroll(user_id, course_id, enroll_data)
           enroll = EnrollSchema.from_orm(course_is_enroll).dict()
           return Response(success=True, message="Enrollment complate", data=enroll)   
       except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))