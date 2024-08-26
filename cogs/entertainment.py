import random
import discord
import asyncio
import requests
from discord import app_commands
from discord.ext import commands


class Entertainment(commands.Cog):
    """Holds all entertainment commands that exsist entirely for fun and don't have a more specific purpose"""

    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client

    def get_hug_gif(self) -> str | None:
        """Retrieves information from an api.
        Simply returns a string or None if the request fails.
        The string will be a url to an anime gif hug."""

        hug_api_url = "https://api.otakugifs.xyz/gif?reaction=hug"
        data = requests.get(hug_api_url)
        return data.json().get("url")

    @app_commands.command(name="hug", description="Give a user of your choice a hug")
    @app_commands.describe(user="The user you want to give a hug to")
    async def _hug(self, interaction: discord.Interaction, user: discord.Member):
        """Takes in a discord.Member object and allows one user to "hug" another.
        This command will send an embed in a nice format with an anime hugging gif.
        It will also ping the member and attempt to access the interaction user's avatar.
        """

        await interaction.response.defer()

        active_event_loop = asyncio.get_running_loop()
        api_results = await active_event_loop.run_in_executor(None, self.get_hug_gif)

        hug_message = f"*{interaction.user.name} is giving {user.name} a hug!*"
        if user == interaction.user or user == self.client.user:
            hug_message = f"Awh, are you lonely {interaction.user.name}? Have some hugs from me! 💙"

        hug_embed = discord.Embed(title="Hugs!", color=0x1D83A5)
        hug_embed.description = hug_message
        hug_embed.set_image(url=api_results)

        try:
            avatar_url = interaction.user.avatar.url
        except Exception as e:
            print(e)
            avatar_url = ""

        hug_embed.set_footer(
            text=f"Hugs from {interaction.user.name}!", icon_url=avatar_url
        )

        await interaction.followup.send(user.mention, embed=hug_embed)

    @app_commands.command(name="flip", description="flip a coin")
    async def _flip(self, interaction: discord.Interaction):
        """Generates a random number; either 0 or 1.
        1 -> Heads
        0 -> Tails"""

        random_number = random.randint(0, 1)
        await interaction.response.send_message(
            f"{interaction.user.mention} {'heads' if random_number else 'tails'}"
        )

    @app_commands.command(name="ping", description="Pong! 🏓")
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong! 🏓", ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Entertainment(client))
