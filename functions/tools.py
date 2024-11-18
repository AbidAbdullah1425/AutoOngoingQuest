import os
import shutil
import requests
from libs.logger import LOGS

class Tools:
    def __init__(self):
        pass

    def rename_file(self, input_file, output_file):
        """Renames the file."""
        try:
            LOGS.info(f"Renaming file from {input_file} to {output_file}.")
            os.rename(input_file, output_file)
            LOGS.info(f"File renamed successfully to {output_file}.")
            return True, "File renamed successfully"
        except Exception as e:
            LOGS.error(f"Error renaming file: {str(e)}")
            return False, str(e)

    def compress(self, input_file, output_file):
        """Placeholder for compression (no compression needed)."""
        try:
            shutil.copy(input_file, output_file)
            LOGS.info(f"File copied (no compression): {input_file} to {output_file}.")
            return True, output_file
        except Exception as e:
            LOGS.error(f"Error copying file: {str(e)}")
            return False, str(e)

    def cover_dl(self, cover_url):
        """Download cover image."""
        try:
            LOGS.info(f"Downloading cover image from {cover_url}.")
            response = requests.get(cover_url, stream=True)
            if response.status_code == 200:
                cover_path = "thumb.jpg"
                with open(cover_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                LOGS.info(f"Cover image downloaded successfully to {cover_path}.")
                return cover_path
            return None
        except Exception as e:
            LOGS.error(f"Error downloading cover image: {str(e)}")
            return None
