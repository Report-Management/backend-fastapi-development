from supabase import create_client
from datetime import datetime
from fastapi import UploadFile, File
import os

class SupabaseService:
    def __init__(self):
        self.__url = "https://uazzhgvzukwpifcufyfg.supabase.co"
        self.__key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVhenpoZ3Z6dWt3cGlmY3VmeWZnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODkxMjUyMCwiZXhwIjoyMDE0NDg4NTIwfQ.GGxJRfo2QcP-0d-23iF9kOM9rOjN4hRrvV5nnrIkLQA"
        self.__storage_bucket = "report"
        self.supabase = create_client(self.__url, self.__key)

    @staticmethod
    def upload_file(bucket: str, file: UploadFile, report_id: str) -> str:
        if bucket is None:
            bucket = SupabaseService().__storage_bucket

        file_name = f"{report_id}.{file.filename.split('.')[-1]}"
        file_content = file.file.read()
        response = SupabaseService().supabase.storage.from_(bucket).upload(
            path=file_name,
            file=file_content,
            file_options={
                'content-type': file.content_type,
            }
        )
        if response.status_code == 200:
            image_url = SupabaseService().supabase.storage.from_(bucket).get_public_url(file_name)
            return image_url.removesuffix('?')
        return None

    @staticmethod
    def delete_image(bucket: str, report_id: str) -> bool:
        if bucket is None:
            bucket = SupabaseService().__storage_bucket
        file_name = f"{report_id}.png"
        response = SupabaseService().supabase.storage.from_(bucket).remove(file_name)
        if response is not []:
            return True
        return False

    @staticmethod
    def is_file_exist(bucket: str, filename: str):
        if bucket is None:
            bucket = SupabaseService().__storage_bucket

        filename = f"{filename}.png"
        response = SupabaseService().supabase.storage.from_(bucket).list()
        if response is []:
            return False

        for image in response:
            if image['name'] == filename:
                return True
        return False

    @staticmethod
    def delete_user(id: str):
        try:
            SupabaseService().supabase.auth.admin.delete_user(id)
            return True
        except Exception as e:
            print("From supabase: ", e)
            return False
