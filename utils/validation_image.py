from fastapi import UploadFile, HTTPException
from typing import List
import magic  # pip install python-magic

# Function to validate file type
def validate_file_type(file: UploadFile, allowed_types: List[str]):
    # Read first 2048 bytes to determine file type
    file_head = file.file.read(2048)
    file.file.seek(0)  # Reset file pointer
    
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_head)
    
    if file_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_type} not allowed. Allowed types are: {allowed_types}"
        )