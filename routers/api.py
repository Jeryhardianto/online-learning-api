from fastapi import APIRouter
from routers.v1 import auth, question, course, instructor, enroll, module, lesson, quiz

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(auth.router)
router.include_router(course.router)
router.include_router(instructor.router)
router.include_router(enroll.router)
router.include_router(module.router)
router.include_router(lesson.router)
router.include_router(quiz.router)
router.include_router(question.router)