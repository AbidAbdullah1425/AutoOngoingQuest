import os
import shutil
from traceback import format_exc
from telethon import Button
from core.bot import LOGS, Bot, Var
from database import DataBase
from functions.info import AnimeInfo
from functions.tools import Tools
from libs.logger import Reporter

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
            rename = await self.anime_info.rename(self.is_original)
            self.output_file = f"encode/{rename}"
            thumb = await self.tools.cover_dl((await self.anime_info.get_poster()))
            if self.is_original:
                await self.reporter.started_renaming()
                succ, out = await self.tools.rename_file(
                    self.input_file, self.output_file
                )
                if not succ:
                    self.logger.error(f"Error renaming file: {out}")
                    return False, out
            else:
                _log_msg = await self.reporter.started_compressing()
                succ, _new_msg = await self.tools.compress(
                    self.input_file, self.output_file, _log_msg
                )
                if not succ:
                    self.logger.error(f"Error compressing file: {_new_msg}")
                    return False, _new_msg
                self.reporter.msg = _new_msg
            await self.reporter.started_uploading()
            msg = await self.bot.upload_anime(
                self.output_file, rename, thumb or "thumb.jpg"
            )
            self.msg_id = msg.id
            self.logger.info(f"File uploaded successfully with ID {self.msg_id}.")
            return True, []
        except BaseException:
            error_msg = str(format_exc())
            self.logger.error(f"Error during execution: {error_msg}")
            await self.reporter.report_error(error_msg, log=True)
            return False, error_msg

    def run_further_work(self):
        asyncio.run(self.further_work())

    async def further_work(self):
        try:
            if self.msg_id:
                await self.reporter.started_gen_ss()
                msg = await self.bot.get_messages(
                    Var.MAIN_CHANNEL,
                    ids=self.msg_id,
                )
                btn = [
                    [],
                ]
                _hash = "hash_generated"
                ss_path, sp_path = await self.tools.gen_ss_sam(_hash, self.output_file)
                if ss_path and sp_path:
                    ss = await self.bot.send_message(
                        Var.CLOUD_CHANNEL,
                        file=glob(f"{ss_path}/*") or ["assest/poster_not_found.jpg"],
                    )
                    sp = await self.bot.send_message(
                        Var.CLOUD_CHANNEL,
                        file=sp_path,
                        thumb="thumb.jpg",
                        force_document=True,
                    )
                    await self.db.store_items(_hash, [[
