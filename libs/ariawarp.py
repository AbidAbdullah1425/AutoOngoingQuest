import subprocess
import os

class AriaWrap:
    def __init__(self):
        self.aria2c = "aria2c"

    def download(self, url, dest_folder):
        try:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            command = [
                self.aria2c,
                "--dir=" + dest_folder,
                "--out=" + url.split("/")[-1],
                url,
            ]
            subprocess.run(command, check=True)
            return True, f"Downloaded to {dest_folder}/{url.split('/')[-1]}"
        except Exception as e:
            return False, str(e)
