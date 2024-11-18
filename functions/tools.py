import requests
import shutil
import os

class Tools:
    def __init__(self):
        pass

    def cover_dl(self, cover_url):
        try:
            response = requests.get(cover_url, stream=True)
            if response.status_code == 200:
                cover_path = "thumb.jpg"
                with open(cover_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                return cover_path
            return None
        except Exception as e:
            return None, str(e)

    def rename_file(self, input_file, output_file):
        try:
            os.rename(input_file, output_file)
            return True, output_file
        except Exception as e:
            return False, str(e)

    def compress(self, input_file, output_file):
        # We are not using any compression, so this is a placeholder
        try:
            shutil.copy(input_file, output_file)
            return True, output_file
        except Exception as e:
            return False, str(e)

    def gen_ss_sam(self, _hash, file_path):
        # Removed screenshot generation functionality as it's not needed
        return None, None
