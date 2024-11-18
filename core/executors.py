import asyncio
import os
import secrets
import shutil
from glob import glob
from traceback import format_exc

from telethon import Button

from core.bot import LOGS, Bot, Var
from database import DataBase
from functions.info import AnimeInfo
from functions.tools import Tools
from libs.logger import Reporter
from libs.ariawrap import aria2_download  # Import for downloading

class Executors:
    def __init__(
        self,
        bot: Bot,
        dB: DataBase,
        configurations: dict,
        input_file: str,
        info: AnimeInfo,
        reporter: Reporter,
    ):
        self.is_original = configurations.get("original_upload")
        self.is_button = configurations.get("button_upload")
        self.anime_info = info
        self.bot = bot
        self.input_file = input_file
        self.tools = Tools()
        self.db = dB
        self.reporter = reporter
        self.msg_id = None
        self.output_file = None

    async def execute(self):
        try:
            # 1. Download the anime episode (no renaming, no compressing)
            rename = await self.anime_info.rename(self.is_original)
            self.output_file = f"encode/{rename}"
            thumb = await self.tools.cover_dl((await self.anime_info.get_poster()))
            
            # 2. Directly download the episode (480p version)
            file_path = await aria2_download(self.anime_info.data["anime_url"], "480p")

            # 3. Upload to Telegram
            await self.reporter.started_uploading()

            # Upload with the correct caption and possibly buttons
            msg = await self.bot.upload_anime(
                file_path, rename, thumb or "thumb.jpg"
            )

            self.msg_id = msg.id

            if self.is_button:
                # Generate buttons for download and other options
                btn = Button.url(
                    f"{self.anime_info.data.get('video_resolution')}",
                    url=f"https://t.me/{((await self.bot.get_me()).username)}?start={msg.id}",
                )
                return True, btn

            return True, []

        except BaseException:
            await self.reporter.report_error(str(format_exc()), log=True)
            return False, str(format_exc())

    def run_further_work(self):
        asyncio.run(self.further_work())

    async def further_work(self):
        try:
            if self.msg_id:
                # Proceed without screenshots or media info
                msg = await self.bot.get_messages(
                    Var.BACKUP_CHANNEL if self.is_button else Var.MAIN_CHANNEL,
                    ids=self.msg_id,
                )
                btn = [
                    [],
                ]

                # No media info or screenshots functionality
                await msg.edit(buttons=btn)

                # Store and cleanup
                _hash = secrets.token_hex(nbytes=7)
                try:
                    shutil.rmtree(_hash)
                    os.remove(self.input_file)
                    os.remove(self.output_file)
                except BaseException:
                    LOGS.error(str(format_exc()))

            await self.reporter.all_done()

        except BaseException:
            await self.reporter.report_error(str(format_exc()), log=True)