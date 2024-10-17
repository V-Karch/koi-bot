import json
import discord
import subprocess
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from pythondebuglogger.Logger import Logger
from models.retro_game_info_view import RetroGameInfoView
from logger_help import send_followup_message_with_logs, defer_with_logs

blue = 0x73BCF8  # Hex color blue stored for embed usage
logger: Logger = Logger(enable_timestamps=True)


class Retroachievements(commands.Cog):
    """Contains all commands related to retroachievements"""

    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

    @app_commands.command(
        name="retro-profile",
        description="get a users profile from retroachievements if it exists",
    )
    @app_commands.describe(
        username="The retroachievements username of the person you want to lookup"
    )
    async def retro_profile(self, interaction: discord.Interaction, username: str):
        logger.display_notice(f"[User {interaction.user.id}] is running /retro_profile")

        # Runs a script in js to fetch the user data and captures it's stdout to display
        await defer_with_logs(interaction, logger)

        # Fetching data from javascript API
        logger.display_notice(
            f"[User {interaction.user.id}/retro_profile] calling getUserProfile.mjs subprocess"
        )
        try:
            profile_stdout = subprocess.check_output(
                f"node cogs/retroachievements-js/getUserProfile.mjs {username}",
                shell=True,
            )
            modified_profile_stdout: str = profile_stdout.decode("utf-8")
            dict_profile_stdout: dict = json.loads(modified_profile_stdout)
        except Exception as e:
            logger.display_error(
                f"[User {interaction.user.id}/retro_profile] raised an error attempting to run getUserProfile.mjs"
            )
            logger.display_debug(e)

        try:
            game_info_and_progress_stdout = subprocess.check_output(
                f"node cogs/retroachievements-js/getGameInfoAndUserProgress.mjs {username} {dict_profile_stdout.get('lastGameId')}",
                shell=True,
            )
            modified_game_info_and_progress_stdout: str = (
                game_info_and_progress_stdout.decode("utf-8")
            )
            dict_game_info_and_progress_stdout: dict = json.loads(
                modified_game_info_and_progress_stdout
            )
        except Exception as e:
            logger.display_error(
                f"[User {interaction.user.id}/retro_profile] raised an error attempting to run getGameInfoAndProgress.mjs"
            )
            logger.display_debug(e)

        # Setting up embed variables
        profile_picture_url: str = (
            "https://media.retroachievements.org" + dict_profile_stdout.get("userPic")
        )
        member_since_as_datetime: datetime = datetime.strptime(
            dict_profile_stdout.get("memberSince"), "%Y-%m-%d %H:%M:%S"
        )
        mastery_percentage = int(
            dict_game_info_and_progress_stdout.get("userCompletionHardcore").split(".")[
                0
            ]
        )

        logger.display_notice(
            f"[User {interaction.user.id}/retro_profile] starting embed creation"
        )
        # Creating embed
        output_embed: discord.Embed = discord.Embed(
            color=blue,
            title="Retro Profile for " + dict_profile_stdout.get("user"),
            description="",
        )
        output_embed.set_thumbnail(url=profile_picture_url)
        output_embed.set_footer(
            text=f"Member since {member_since_as_datetime.strftime('%B %d, %Y')}"
        )
        output_embed.description += f"Last Game Played: **{dict_game_info_and_progress_stdout.get('title')} ({mastery_percentage}%)**\n"
        output_embed.description += f"-# {dict_profile_stdout.get('richPresenceMsg')}\n"
        output_embed.description += f"**__{dict_profile_stdout.get('totalPoints')}__ ({dict_profile_stdout.get('totalTruePoints')})** total points.\n"
        logger.display_notice(
            f"[User {interaction.user.id}/retro_profile] embed created"
        )

        # Create View
        output_view: discord.ui.View = RetroGameInfoView(
            dict_game_info_and_progress_stdout
        )

        # Sending response
        await send_followup_message_with_logs(
            interaction, logger, "retro_profile", embed=output_embed, view=output_view
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Retroachievements(client))
