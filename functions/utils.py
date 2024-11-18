import os
import asyncio
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

    async def upload_episode_to_telegram(self, file, caption):
        """Upload the anime episode to the Telegram channel."""
        try:
            message = await self.bot.send_document(
                Var.MAIN_CHANNEL,
                file,
                caption=caption,
                force_document=True,
            )
            return message
        except Exception as e:
            LOGS.error(f"Failed to upload episode: {str(e)}")
            return None

    async def create_buttons(self, file_id):
        """Create a button to allow users to download the file from Telegram."""
        download_link = f"https://t.me/{self.bot.username}?start={file_id}"
        try:
            return [
                Button.url("Download 480p", download_link)
            ]
        except Exception as e:
            LOGS.error(f"Failed to create buttons: {str(e)}")
            return []

    async def send_episode_with_buttons(self, file, caption):
        """Upload the episode and send a download link with buttons."""
        try:
            # Upload the episode to Telegram
            message = await self.upload_episode_to_telegram(file, caption)

            # Generate the download link and create buttons
            download_link = f"https://t.me/{self.bot.username}?start={message.id}"
            buttons = await self.create_buttons(message.id)

            # Edit the message to include buttons
            await self.bot.edit_message_text(
                message.chat.id,
                message.id,
                caption,
                reply_markup=buttons
            )

            return message
        except Exception as e:
            LOGS.error(f"Failed to send episode with buttons: {str(e)}")
            return None

    async def force_subscription_check(self, user_id):
        """Check if the user is subscribed to the required channel."""
        try:
            is_subscribed = await self.bot.is_member(Var.FORCESUB_CHANNEL, user_id)
            if not is_subscribed:
                return False
            return True
        except Exception as e:
            LOGS.error(f"Failed to check subscription: {str(e)}")
            return False
