from datetime import datetime
from typing import Optional
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from enums.enum_tipe import IsDone
from schemas.common_shcema import TokenData
from schemas.todo_schema import OutputTransactionPage, TodoCreate, TodoIsDone, TodoUpdate
from services.service_common import get_current_user
from services.service_todo import ServiceTodo
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todo", tags=["Todos"])

@router.get("")
def get_all_todo(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    status: Optional[IsDone] = None,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(get_db)
):
    service_todo = ServiceTodo(session)
    return service_todo.get_list_todo(status, page, size, current_user)

@router.get("/{id}")
def get_todo_by_id(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_todo = ServiceTodo(session)
    return service_todo.get_by_id(id, current_user)

@router.post("")
def insert_todo(
   input_todo: TodoCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_todo = ServiceTodo(session)
  return service_todo.insert(input_todo, current_user)

@router.put("/{id}")
def update_todo(
    id: int,
    input_todo: TodoUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_todo = ServiceTodo(session)
    return service_todo.update(id, input_todo, current_user)

@router.patch("/{id}/is_done")
def is_done_todo(
    id: int,
    input_todo: TodoIsDone,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_todo = ServiceTodo(session)
    return service_todo.is_done(id, input_todo, current_user)

@router.delete("/{id}")
def delete_todo(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_todo = ServiceTodo(session)
    return service_todo.delete(id, current_user)

# @router_transaction.post("/export")
# def export_history_transaction(
#     current_user: Annotated[TokenData, Depends(get_current_user)],
#     start_date: Optional[datetime] = None,
#     end_date: Optional[datetime] = None,
#     tipe: Optional[TipeEnum] = None,
#     service_transaction: ServiceTransaction = Depends(),
# ):
#     if start_date is None or end_date is None:
#         start_date = None
#         end_date = None
#     else:
#          # Check if start_date and end_date are not already datetime objects
#         if not isinstance(start_date, datetime):
#             start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         if not isinstance(end_date, datetime):
#             end_date = datetime.strptime(end_date, "%Y-%m-%d")

#     content_file, file_name = service_transaction.export_transaction(
#         tipe, start_date, end_date, current_user
#     )

#     print(content_file)

#     headers = {"Content-Disposition": f"attachment; filename={file_name}"}
#     return StreamingResponse(iter([content_file]), headers=headers)