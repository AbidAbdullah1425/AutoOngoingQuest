import os
import shutil
import asyncio
from glob import glob
from pyrogram import Client
from telethon import Button

from libs.logger import LOGS
from functions.config import Var
from libs.subsplease import SubsPlease
from libs.kitsu import Kitsu


class Utils:
    def __init__(self, bot: Client):
        self.bot = bot
        self.subsplease = SubsPlease()
        self.kitsu = Kitsu()

    async def download_episode(self, rss_url):
        """Download the anime episode from RSS Feed."""
        try:
            episode = await self.subsplease.fetch_episode(rss_url)
            download_link = await self.subsplease.download_episode(episode)
            return download_link
        except Exception as e:
            LOGS.error(f"Failed to download episode: {str(e)}")
            return None

    async def generate_download_link(self, file):
        """Generate file download link for Telegram."""
        try:
            file_hash = self.generate_hash(file)
            _hash = secrets.token_hex(nbytes=7)
            download_link = f"https://t.me/{self.bot.username}?start={_hash}"
            # Store the file and link in the database
            await self.bot.db.store_items(_hash, [file.id])
            return download_link
        except Exception as e:
            LOGS.error(f"Failed to generate download link: {str(e)}")
            return None

    def generate_hash(self, file):
        """Generate a hash for the given file."""
        return file.file_id[:16]

    async def send_episode(self, file, caption, is_button=False):
        """Send the anime episode to the channel."""
        try:
            message = await self.bot.send_document(
                Var.MAIN_CHANNEL,
                file,
                caption=caption,
                force_document=True,
            )
            return message
        except Exception as e:
            LOGS.error(f"Failed to send episode: {str(e)}")
            return None

    async def create_buttons(self, download_link):
        """Create the button for downloading the episode."""
        try:
            return [
                Button.url("Download 480p", download_link)
            ]
        except Exception as e:
            LOGS.error(f"Failed to create buttons: {str(e)}")
            return []

    async def clean_up(self, file_path):
        """Clean up downloaded and processed files."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                LOGS.warning(f"File not found: {file_path}")
        except Exception as e:
            LOGS.error(f"Failed to clean up file: {str(e)}")
