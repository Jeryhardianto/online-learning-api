from fastapi import APIRouter
from routers.v1 import auth, todo, course

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(auth.router)
router.include_router(course.router)
# router.include_router(todo.router)