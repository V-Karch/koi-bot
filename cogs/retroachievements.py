import json
import asyncio
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
        description="get a user's profile from retroachievements if it exists",
    )
    @app_commands.describe(
        username="The retroachievements username of the person you want to lookup"
    )
    async def retro_profile(self, interaction: discord.Interaction, username: str):
        logger.display_notice(f"[User {interaction.user.id}] is running /retro_profile")

        await defer_with_logs(interaction, logger)

        # Initialize with default values
        dict_profile_stdout: dict = {}
        dict_game_info_and_progress_stdout: dict = {}

        # Step 1: Get user profile
        try:
            logger.display_notice(
                f"[User {interaction.user.id}/retro_profile] calling getUserProfile.mjs subprocess"
            )
            profile_stdout = await asyncio.create_subprocess_exec("node", "cogs/retroachievements-js/getUserProfile.mjs", username)

            profile_stdout = subprocess.check_output(
                f"node cogs/retroachievements-js/getUserProfile.mjs {username}",
                shell=True,
            )
            modified_profile_stdout = profile_stdout.decode("utf-8")
            dict_profile_stdout = json.loads(modified_profile_stdout)
        except Exception as e:
            logger.display_error(
                f"[User {interaction.user.id}/retro_profile] failed in getUserProfile.mjs"
            )
            logger.display_debug(str(e))
            await send_followup_message_with_logs(
                interaction,
                logger,
                "retro_profile",
                message=f"❌ Could not retrieve profile for `{username}`. Please check the username or try again later.",
            )
            return

        # Step 2: Get game info and progress
        try:
            last_game_id = dict_profile_stdout.get("lastGameId")
            if not last_game_id:
                raise ValueError("Missing lastGameId from profile data.")

            game_info_and_progress_stdout = subprocess.check_output(
                f"node cogs/retroachievements-js/getGameInfoAndUserProgress.mjs {username} {last_game_id}",
                shell=True,
            )
            modified_game_info_and_progress_stdout = (
                game_info_and_progress_stdout.decode("utf-8")
            )
            dict_game_info_and_progress_stdout = json.loads(
                modified_game_info_and_progress_stdout
            )
        except Exception as e:
            logger.display_error(
                f"[User {interaction.user.id}/retro_profile] failed in getGameInfoAndProgress.mjs"
            )
            logger.display_debug(str(e))
            await send_followup_message_with_logs(
                interaction,
                logger,
                "retro_profile",
                message=f"⚠️ Could retrieve profile for `{username}` but failed to get recent game information.",
            )
            return

        # Step 3: Construct embed
        try:
            logger.display_notice(
                f"[User {interaction.user.id}/retro_profile] starting embed creation"
            )

            profile_picture_url = (
                "https://media.retroachievements.org"
                + dict_profile_stdout.get("userPic", "")
            )
            member_since_as_datetime = datetime.strptime(
                dict_profile_stdout.get("memberSince", "2000-01-01 00:00:00"),
                "%Y-%m-%d %H:%M:%S",
            )
            mastery_percentage = int(
                dict_game_info_and_progress_stdout.get(
                    "userCompletionHardcore", "0"
                ).split(".")[0]
            )

            output_embed = discord.Embed(
                color=blue,
                title="Retro Profile for " + dict_profile_stdout.get("user", username),
                description="",
            )
            output_embed.set_thumbnail(url=profile_picture_url)
            output_embed.set_footer(
                text=f"Member since {member_since_as_datetime.strftime('%B %d, %Y')}"
            )
            output_embed.description += (
                f"Last Game Played: **{dict_game_info_and_progress_stdout.get('title', 'Unknown')} "
                f"({mastery_percentage}%)**\n"
            )  # type: ignore
            output_embed.description += f"-# {dict_profile_stdout.get('richPresenceMsg', 'No rich presence available')}\n"
            output_embed.description += (
                f"**__{dict_profile_stdout.get('totalPoints', '0')}__ "
                f"({dict_profile_stdout.get('totalTruePoints', '0')})** total points.\n"
            )

            logger.display_notice(
                f"[User {interaction.user.id}/retro_profile] embed created"
            )

            output_view = RetroGameInfoView(dict_game_info_and_progress_stdout)

            await send_followup_message_with_logs(
                interaction,
                logger,
                "retro_profile",
                embed=output_embed,
                view=output_view,
            )

        except Exception as e:
            logger.display_error(
                f"[User {interaction.user.id}/retro_profile] failed to build or send embed"
            )
            logger.display_debug(str(e))
            await send_followup_message_with_logs(
                interaction,
                logger,
                "retro_profile",
                message="⚠️ Something went wrong while preparing the response. Please try again later.",
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Retroachievements(client))
