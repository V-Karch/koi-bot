import random
import discord
import asyncio
import requests
from discord import app_commands
from discord.ext import commands
from pythondebuglogger.Logger import Logger
from logger_help import (
    defer_with_logs,
    send_followup_message_with_logs,
    send_response_message_with_logs,
)

logger: Logger = Logger(enable_timestamps=True)  # Create the debug logger


class Entertainment(commands.Cog):
    """Holds all entertainment commands that exsist entirely for fun and don't have a more specific purpose"""

    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client

    def get_hug_gif(self) -> str | None:
        """Retrieves information from an api.
        Simply returns a string or None if the request fails.
        The string will be a url to an anime gif hug."""

        hug_api_url = "https://api.otakugifs.xyz/gif?reaction=hug"
        logger.display_notice("[get_hug_gif()] Attempting to request data from API")
        data = requests.get(hug_api_url)

        try:
            url = data.json().get("url")
            logger.display_notice(
                "[get_hug_gif()] Successfully requested data from API"
            )
            return url
        except Exception as e:
            logger.display_error(
                f"[get_hug_gif()] failed to retrieve a valid json response: {e}"
            )
            logger.display_error("[get_hug_gif()] Actual response data:")
            logger.display_debug(data.text)
            return None

    @app_commands.command(name="hug", description="Give a user of your choice a hug")
    @app_commands.describe(user="The user you want to give a hug to")
    async def _hug(self, interaction: discord.Interaction, user: discord.Member):
        """Takes in a discord.Member object and allows one user to "hug" another.
        This command will send an embed in a nice format with an anime hugging gif.
        It will also ping the member and attempt to access the interaction user's avatar.
        """

        logger.display_notice(f"[User {interaction.user.id}] is calling /hug")

        await defer_with_logs(interaction, logger)

        try:
            active_event_loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.display_error(
                f"[User {interaction.user.id}/hug] There is no running event loop."
            )
            return

        logger.display_notice(f"[User {interaction.user.id}/hug] calling get_hug_gif()")
        api_results = await active_event_loop.run_in_executor(None, self.get_hug_gif)

        if api_results is None:
            logger.display_error(
                f"[User {interaction.user.id}/hug] Failed to retrieve valid json from API"
            )
            return

        logger.display_notice(f"[User {interaction.user.id}/hug] creating hug embed")
        hug_message = f"*{interaction.user.name} is giving {user.name} a hug!*"
        if user == interaction.user or user == self.client.user:
            hug_message = f"Awh, are you lonely {interaction.user.name}? Have some hugs from me! 💙"

        hug_embed = discord.Embed(title="Hugs!", color=0x1D83A5)
        hug_embed.description = hug_message
        hug_embed.set_image(url=api_results)

        try:
            avatar_url = interaction.user.avatar.url  # type: ignore
        except Exception:
            logger.display_debug(
                f"[User {interaction.user.id}/hug] Something is up with the users avatar."
            )
            avatar_url = ""

        hug_embed.set_footer(
            text=f"Hugs from {interaction.user.name}!", icon_url=avatar_url
        )

        await send_followup_message_with_logs(
            interaction, logger, "hug", user.mention, hug_embed
        )

    @app_commands.command(name="flip", description="flip a coin")
    async def _flip(self, interaction: discord.Interaction):
        """Generates a random number; either 0 or 1.
        1 -> Heads
        0 -> Tails"""

        logger.display_notice(f"[User {interaction.user.id}] is calling /flip")
        random_number = random.randint(0, 1)
        logger.display_notice(
            f"[User {interaction.user.id}] generated random number ({random_number})"
        )

        await send_response_message_with_logs(
            interaction,
            logger,
            "flip",
            f"{interaction.user.mention} {'heads' if random_number else 'tails'}",
        )

    @app_commands.command(name="ping", description="Pong! 🏓")
    async def _ping(self, interaction: discord.Interaction):
        logger.display_notice(f"[User {interaction.user.id}] is calling /ping")

        await send_response_message_with_logs(
            interaction, logger, "ping", "Pong! 🏓", ephemeral=True
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Entertainment(client))
