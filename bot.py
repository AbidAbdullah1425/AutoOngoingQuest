import asyncio
import sys
from logging import Logger
from traceback import format_exc
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from functions.config import Var
from libs.logger import LOGS, TelethonLogger

class Bot(Client):
    def __init__(
        self,
        api_id=None,
        api_hash=None,
        bot_token=None,
        logger: Logger = LOGS,
        log_attempt=True,
        exit_on_error=True,
        *args,
        **kwargs,
    ):
        self._handle_error = exit_on_error
        self._log_at = log_attempt
        self.logger = logger
        kwargs["api_id"] = api_id or Var.API_ID
        kwargs["api_hash"] = api_hash or Var.API_HASH
        kwargs["base_logger"] = TelethonLogger
        super().__init__(None, **kwargs)
        self.pyro_client = Client(
            name="pekka",
            api_id=kwargs["api_id"],
            api_hash=kwargs["api_hash"],
            bot_token=bot_token or Var.BOT_TOKEN,
            in_memory=True,
        )
        self.user_client = None
        if Var.SESSION:
            self.user_client = TelegramClient(
                StringSession(Var.SESSION), kwargs["api_id"], kwargs["api_hash"]
            )
        self.run_in_loop(self.start_client(bot_token=bot_token or Var.BOT_TOKEN))

    def __repr__(self):
        return f"<AnimeBot.Client : bot: {self._bot}>"

    async def start_client(self, **kwargs):
        """Function to start the client."""
        if self._log_at:
            self.logger.info("Attempting to login to Telegram.")
        try:
            await self.start(**kwargs)
            if self.user_client:
                await self.user_client.start()
            await self.pyro_client.start()
            self.logger.info("Successfully logged in.")
        except Exception as e:
            self.logger.critical(f"Error while logging in: {str(e)}")
            sys.exit(1)

    async def is_joined(self, channel_id, user_id):
        """Check if the user is a member of the forced subscription channel."""
        try:
            await self.pyro_client.get_participant(channel_id, user_id)
            self.logger.info(f"User {user_id} is already subscribed to {channel_id}.")
            return True
        except UserNotParticipantError:
            self.logger.warning(f"User {user_id} is NOT subscribed to {channel_id}.")
            return False

    async def force_subscribe(self, user_id):
        """Force the user to subscribe to the channel if they aren't already."""
        if not await self.is_joined(Var.FORCE_SUB_CHANNEL, user_id):
            link = await self.generate_invite_link(Var.FORCE_SUB_CHANNEL)
            await self.send_message(
                user_id,
                f"Please join the channel to get access: {link}",
            )
            self.logger.info(f"Sent subscription reminder to {user_id}.")
            return False
        self.logger.info(f"User {user_id} has subscribed successfully.")
        return True

    async def generate_invite_link(self, channel_id):
        """Generate an invite link for a channel."""
        try:
            invite = await self.pyro_client.export_chat_invite_link(channel_id)
            return invite
        except Exception as e:
            self.logger.error(f"Failed to generate invite link: {str(e)}")
            return ""

    async def upload_anime(self, file, caption, thumb=None, is_button=False):
        """Upload the anime episode to Telegram with the given caption and thumbnail."""
        if not self.pyro_client.is_connected:
            await self.pyro_client.connect()
        self.logger.info(f"Uploading file {file} to {Var.MAIN_CHANNEL}.")
        post = await self.pyro_client.send_document(
            Var.MAIN_CHANNEL,  # Using main channel directly for 480p uploads
            file,
            caption=f"`{caption}`",
            force_document=True,
            thumb=thumb or "thumb.jpg",
        )
        self.logger.info(f"Uploaded file successfully with message ID {post.id}.")
        return post

    def run_in_loop(self, function):
        """Run the function inside the event loop."""
        return self.loop.run_until_complete(function)

    def run(self):
        """Run the bot until disconnected."""
        self.run_until_disconnected()

    def add_handler(self, func, *args, **kwargs):
        """Add an event handler for the bot."""
        if func in [_[0] for _ in self.list_event_handlers()]:
            return
        self.add_event_handler(func, *args, **kwargs)
