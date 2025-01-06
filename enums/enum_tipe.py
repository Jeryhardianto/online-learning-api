from enum import Enum

# enum
class IsDone(str, Enum):
    def __str__(self):
        return str(self.value)
    INPROGRESS = "IN PROGRESS"
    DONE = "DONE"

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class EnrollmentStatus(str, Enum):
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"