from supabase import create_client
from datetime import datetime
from fastapi import UploadFile

class SupabaseService:
    def __init__(self):
        self.__url = "https://uazzhgvzukwpifcufyfg.supabase.co"
        self.__key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVhenpoZ3Z6dWt3cGlmY3VmeWZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTg5MTI1MjAsImV4cCI6MjAxNDQ4ODUyMH0.-PNxIN4W6k9wSpcUQ75t8YjGDpofXOWk3jgL0wEDNNo"
        self.__storage_bucket = "report"
        self.supabase = create_client(self.__url, self.__key)

    @staticmethod
    def upload_image(bucket: str, file: UploadFile, report_id: str) -> str:
        if bucket is None:
            bucket = SupabaseService().__storage_bucket

        file_name = f"{report_id}.png"
        file_content = file.file.read()
        response = SupabaseService().supabase.storage.from_(bucket).upload(
            path=file_name,
            file=file_content,
            file_options={
                'content-type': "image/png"
            }
        )

        if response.status_code == 200:
            image_url = SupabaseService().supabase.storage.from_(bucket).get_public_url(file_name)
            return image_url.removesuffix('?')
        return None