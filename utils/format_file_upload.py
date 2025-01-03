import uuid
import os

def format_file_upload(filename):
    # Generate a UUID
    unique_id = uuid.uuid4()

    # Get the file extension
    file_extension = os.path.splitext(filename)[1]

    # Create the new filename with the UUID and the original file extension
    new_filename = f"{unique_id}{file_extension}"

    return new_filename