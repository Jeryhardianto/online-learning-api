import math
from datetime import datetime, timedelta
from typing import Optional

import pandas

from fastapi import Depends, HTTPException
from enums.enum_tipe import IsDone
from models.model_todo import Todo as TodoModel
from repositories.repository_course import RepositoryCourse
from schemas.common_shcema import Response, TokenData
from schemas.course_schema import OutputTransactionPage, Course as CourseSchema
from sqlalchemy.orm import Session


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

        result = OutputTransactionPage(
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
    
    # def insert(
    #     self, todo_data: TodoCreate, current_user: TokenData
    # ):
    #    try:
    #        todo = TodoModel(
    #            title=todo_data.title,
    #            description=todo_data.description,
    #            status=todo_data.status,
    #            user_id=current_user.id,
    #            created_at=datetime.now(),
    #            updated_at=datetime.now()
    #        )
    #        self.repository_todo.store_todo(todo)
    #        todo = TodoSchema.from_orm(todo).dict()
    #        return Response(success=True, message="Todo created", data=todo)   
    #    except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))
       
    # def update(self, id: int, todo_data: TodoUpdate, current_user: TokenData):
    #     found_todo = self.repository_todo.get_by_id(id, current_user.id)
    #     if found_todo is None:
    #         raise HTTPException(status_code=404, detail="Todo not found")
        
    #     try:
    #         todo = self.repository_todo.update(id, todo_data, current_user.id)
    #         todo = TodoSchema.from_orm(todo).dict()
    #         return Response(success=True, message="Todo updated", data=todo)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))
        
    # def is_done(self, id: int, todo_data: TodoIsDone, current_user: TokenData):
    #     found_todo = self.repository_todo.get_by_id(id, current_user.id)
    #     if found_todo is None:
    #         raise HTTPException(status_code=404, detail="Todo not found")
        
    #     try:
    #         todo = self.repository_todo.is_done(id, todo_data, current_user.id)
    #         todo = TodoSchema.from_orm(todo).dict()
    #         return Response(success=True, message="Todo status updated", data=todo)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))

    # def delete(self, id: int, current_user: TokenData):
    #     found_todo = self.repository_todo.get_by_id(id, current_user.id)
    #     if found_todo is None:
    #         raise HTTPException(status_code=404, detail="Todo not found")
        
    #     try:
    #         todo = self.repository_todo.delete(id, current_user.id)
    #         todo = TodoSchema.from_orm(todo).dict()
    #         return Response(success=True, message="Todo deleted", data=todo)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))

        
    # def export_transaction(
    #     self,
    #     tipe: TipeEnum,
    #     start_date: datetime,
    #     end_date: datetime,
    #     current_user: TokenData,
    # ):
    #     match_filter = {"user_id": current_user.userId}
    #     if tipe is not None:
    #         match_filter["tipe"] = tipe

    #     if start_date is not None and end_date is not None:
    #         match_filter["created_time"] = {
    #             "$gte": start_date,
    #             "$lt": end_date + timedelta(days=1),
    #         }

    #     projection_stage = Transaction.project_export()

    #     result = self.repository_transaction.export_list_transaction(
    #         match_filter, projection_stage
    #     )
    #     print(result)

    #     if len(result) == 0:
    #         raise HTTPException(status_code=400, detail="No data to be exported")

    #     df = pandas.DataFrame(result)

    #     file_name = "History_Transaksi.csv"
    #     content_file = df.to_csv(sep=";")
    #     return content_file, file_name
