import asyncio
import os
from pathlib import Path
from datetime import datetime

from aiohttp import ClientSession
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from libs.ariawrap import aria2_download
from libs.logger import LOGS
from libs.subsplease import SubsPlease
from libs.kitsu import Kitsu
from database import DataBase
from functions.config import Var


class Executor:
    def __init__(self, bot: Client):
        self.bot = bot
        self.db = DataBase()

    async def start(self):
        """
        Start the main process to check RSS feed, download episodes and update posts.
        """
        await self.db.toggle_separate_channel_upload()

        while True:
            try:
                await self.check_for_new_episodes()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                LOGS.error(f"Error while processing: {str(e)}")
                await asyncio.sleep(10)

    async def check_for_new_episodes(self):
        """
        Check the RSS feed and process new episodes.
        """
        LOGS.info("Checking for new episodes in RSS feed")
        rss = SubsPlease()
        episodes = await rss.fetch_episodes()

        for episode in episodes:
            anime_title = episode["title"]
            anime_url = episode["url"]
            episode_number = episode["episode"]
            episode_season = episode.get("season", "Unknown")  # Get the season from RSS, if available
            episode_quality = "480p"

            if not await self.db.is_anime_uploaded(anime_title):
                LOGS.info(f"New episode detected: {anime_title} - Episode {episode_number}")
                await self.process_episode(anime_title, anime_url, episode_number, episode_season, episode_quality)
                await self.db.add_anime(anime_title)

    async def process_episode(self, anime_title: str, anime_url: str, episode_number: int, season: str, quality: str):
        """
        Process the anime episode by downloading it, uploading to Telegram, and updating post.
        """
        try:
            LOGS.info(f"Downloading episode {episode_number} of {anime_title}")

            # Download the episode
            file_path = await aria2_download(anime_url, quality)

            # Upload the file to Telegram
            await self.upload_to_telegram(anime_title, episode_number, season, file_path)

            # Update the post with the download link
            await self.update_post_with_link(anime_title, episode_number, season, quality, file_path)

        except Exception as e:
            LOGS.error(f"Error while processing episode {anime_title} - {episode_number}: {str(e)}")

    async def upload_to_telegram(self, anime_title: str, episode_number: int, season: str, file_path: str):
        """
        Upload the downloaded file to Telegram.
        """
        try:
            # Open the file for upload
            with open(file_path, "rb") as f:
                caption = f"✨ Anime Name: {anime_title} | {anime_title} ✨\n" \
                          f"━━━━━━━━━━━━━━━\n" \
                          f"🗣 Language: Japanese\n" \
                          f"📺 Quality: {quality}\n" \
                          f"🍂 Season: {season}\n" \
                          f"📆 Episode: {episode_number}\n" \
                          f"━━━━━━━━━━━━━━━"
                
                # Upload to the appropriate channel
                if Var.MAIN_CHANNEL:
                    await self.bot.send_document(
                        Var.MAIN_CHANNEL,
                        f,
                        caption=caption,
                        reply_markup=None,
                        disable_notification=True
                    )
                    LOGS.info(f"Successfully uploaded episode {episode_number} to channel.")
        except Exception as e:
            LOGS.error(f"Error uploading to Telegram for episode {anime_title} - {episode_number}: {str(e)}")

    async def update_post_with_link(self, anime_title: str, episode_number: int, season: str, quality: str, file_path: str):
        """
        Update the post in Telegram with the download link.
        """
        try:
            # Generate download link
            download_link = f"https://t.me/{Var.BOT_USERNAME}?start={episode_number}"

            # Edit the post with the download link
            message = f"✨ Anime Name: {anime_title} | {anime_title} ✨\n" \
                      f"━━━━━━━━━━━━━━━\n" \
                      f"🗣 Language: Japanese\n" \
                      f"📺 Quality: {quality}\n" \
                      f"🍂 Season: {season}\n" \
                      f"📆 Episode: {episode_number}\n" \
                      f"━━━━━━━━━━━━━━━"

            # Update the original post with the link
            if Var.MAIN_CHANNEL:
                await self.bot.send_message(
                    Var.MAIN_CHANNEL,
                    message,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Download 480p", url=download_link)]]
                    )
                )
            LOGS.info(f"Successfully updated post with download link for episode {anime_title} - {episode_number}.")
        except Exception as e:
            LOGS.error(f"Error updating post for episode {anime_title} - {episode_number}: {str(e)}")
