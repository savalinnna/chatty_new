from fastapi import UploadFile, HTTPException
from core.config import settings
from minio import Minio
from minio.error import S3Error
import uuid

client = Minio(
    settings.s3_endpoint.replace("http://", ""),
    access_key=settings.s3_access_key,
    secret_key=settings.s3_secret_key,
    secure=False
)

async def upload_image_to_s3(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"

    try:
        file_data = await file.read()
        file_size = len(file_data)

        # ensure bucket exists
        found = client.bucket_exists(settings.s3_bucket_name)
        if not found:
            client.make_bucket(settings.s3_bucket_name)

        client.put_object(
            bucket_name=settings.s3_bucket_name,
            object_name=unique_name,
            data=bytes(file_data),
            length=file_size,
            content_type=file.content_type
        )

        return f"{settings.s3_endpoint}/{settings.s3_bucket_name}/{unique_name}"

    except S3Error as err:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {err}")
