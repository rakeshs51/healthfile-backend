# utils/s3_client.py
from pipes import quote
from tempfile import SpooledTemporaryFile
import uuid
import boto3
from fastapi import HTTPException, UploadFile
from ..config import settings
from .s3_client import S3Client
from botocore.exceptions import ClientError

async def upload_file_to_s3(file: UploadFile):
    
    s3_client = S3Client.get_instance() # Get the initialized S3 client instance
    bucket_name = settings.AWS_S3_BUCKET_NAME
    region_name = settings.AWS_REGION_NAME

    try:
        extension = file.filename.split('.')[-1]
        safe_filename = f"{uuid.uuid4()}.{extension}"
        
        # Create a temporary spooled file
        with SpooledTemporaryFile(mode='wb') as temp_file:
            # Read content from UploadFile asynchronously
            content = await file.read()
            # Write content to spooled file
            temp_file.write(content)
            # Important: reset file pointer to the start
            temp_file.seek(0)
            
            file_path = f"uploads/{safe_filename}"

            # Upload the content using the temporary file
            s3_client.upload_fileobj(
                temp_file,
                bucket_name,
                file_path,
                ExtraArgs={'ContentType': file.content_type}
            )

            file_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file_path}"
            return file_url
    
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e}")

