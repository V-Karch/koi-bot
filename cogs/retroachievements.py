import ast
import json
import discord
import subprocess
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from models.retro_game_info_view import RetroGameInfoView

blue = 0x73BCF8  # Hex color blue stored for embed usage

class Retroachievements(commands.Cog):
    """Contains all commands related to retroachievements"""
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot  = client

    @app_commands.command(name = "retro-profile", description = "get a users profile from retroachievements if it exists") 
    @app_commands.describe(username = "The retroachievements username of the person you want to lookup")
    async def retro_profile(self, interaction: discord.Interaction, username: str):
        # Runs a script in js to fetch the user data and captures it's stdout to display
        await interaction.response.defer()

        # Fetching data from javascript API
        profile_stdout = subprocess.check_output(f"node cogs/retroachievements-js/getUserProfile.mjs {username}", shell = True)
        modified_profile_stdout: str = profile_stdout.decode("utf-8")
        dict_profile_stdout: dict = json.loads(modified_profile_stdout)
        game_info_and_progress_stdout = subprocess.check_output(f"node cogs/retroachievements-js/getGameInfoAndUserProgress.mjs {username} {dict_profile_stdout.get('lastGameId')}", shell = True)
        modified_game_info_and_progress_stdout: str = game_info_and_progress_stdout.decode("utf-8")
        dict_game_info_and_progress_stdout: dict = json.loads(modified_game_info_and_progress_stdout)

        # Setting up embed variables
        profile_picture_url: str = "https://media.retroachievements.org" + dict_profile_stdout.get("userPic")
        member_since_as_datetime: datetime = datetime.strptime(dict_profile_stdout.get("memberSince"), "%Y-%m-%d %H:%M:%S")
        mastery_percentage = int(dict_game_info_and_progress_stdout.get('userCompletionHardcore').split(".")[0])

        # Creating embed
        output_embed: discord.Embed = discord.Embed(color = blue, title = "Retro Profile for " + dict_profile_stdout.get("user"), description = "")
        output_embed.set_thumbnail(url = profile_picture_url)
        output_embed.set_footer(text = f"Member since {member_since_as_datetime.strftime('%B %d, %Y')}")
        output_embed.description += f"Last Game Played: **{dict_game_info_and_progress_stdout.get('title')} ({mastery_percentage}%)**\n"
        output_embed.description += f"-# {dict_profile_stdout.get('richPresenceMsg')}\n"
        output_embed.description += f"**__{dict_profile_stdout.get('totalPoints')}__ ({dict_profile_stdout.get('totalTruePoints')})** total points.\n"

        # Create View
        output_view: discord.ui.View = RetroGameInfoView(dict_game_info_and_progress_stdout)

        # Sending response
        await interaction.followup.send(embed = output_embed, view = output_view)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Retroachievements(client))
