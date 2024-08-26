import os
import sys
import base64
import discord
import subprocess
from discord import app_commands
from discord.ext import commands

blue = 0x73BCF8  # Hex color blue stored for embed usage
owner_id = 923600698967461898


class Utilities(commands.Cog):
    """
    Utilites Commands Cog
    Houses all utility commands for the discord bot
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client
        # ^^ Sets the client to be an attribute of the class

    @app_commands.command(name="restart", description="restarts the bot")
    async def restart(self, interaction: discord.Interaction):
        if interaction.user.id != 923600698967461898:
            await interaction.response.send_message("No.")
            return
        
        await interaction.response.send_message("Restarting...")
        os.execv(sys.executable, ["python"] + sys.argv)

    @app_commands.command(name="base64-encode", description="Encodes a given text")
    @app_commands.describe(text="The text to excode to base64")
    async def base64_encode(self, interaction: discord.Interaction, text: str) -> None:
        """
        Takes an input text and converts it to base64 format before
        sending it as a discord embed

        Args:
            interaction (discord.Interaction): Provided automatically by discord, the interaction data from the command
            text (str): Text provided by the command user, to convert to base64

        Returns (None): sends a discord embed as a result and returns nothing 
        """

        await interaction.response.defer(ephemeral=True)  # Wait ephemerally
        embed = discord.Embed(color=blue, title="✅ Base64 Encoded Result")
        # ^^ Create the embed with it's constructor
        text_as_bytes: bytes = base64.b64encode(bytes(text, "utf-8"))
        # ^^ Convert text to base64 bytes
        embed.description = f"```\n{text_as_bytes.decode()}\n```"
        # ^^ Set embed description to text format of base64 bytes
        embed.set_footer(
            text="Requested by @" + interaction.user.name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else "",
        )
        # ^^ Set the embed footer to the one who used to command
        await interaction.followup.send(embed=embed)  # Send the resulting embed

    @app_commands.command(
        name="base64-decode",
        description="Decodes a given base64 string into plain text",
    )
    @app_commands.describe(text="The base64 text to decode to plain text")
    async def base64_decode(self, interaction: discord.Interaction, text: str) -> None:
        """
        Takes a base64 input as a string text and attempts to convert it
        back into plain text.

        Args:
            interaction (discord.Interaction): Provided by discord, the interaction which called the command.
            text (str): The input text, should be given in base64 format

        Returns (None): Sends a discord embed as a result and returns nothing
        """

        await interaction.response.defer(ephemeral=True)  # Waits ephemerally
        embed = discord.Embed(color=blue, title="✅ Base64 Decoded Result")
        # ^^ Create the embed with it's constructor
        try:  # Attempt to convert the base64 input to plain text
            embed.description = f"```\n{str(base64.b64decode(text))[2:-1]}\n```"
            """ ^^ Adds the converted plain text to the embed description
            and converts it in one line.
            If this throws base64.binascii.Error
            An invalid input was given
            """
        except base64.binascii.Error:  # In the case that an invalid input was given
            embed.description = f"```diff\n- Text was not in base64 format\n```"
            # ^^ Change the embed description to reflect that

        embed.set_footer(
            text="Requested by @" + interaction.user.name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else "",
        )
        # ^^ Set the embed footer to reflect the user who called the interaction

        await interaction.followup.send(embed=embed)  # Send the resulting embed

    @app_commands.command(name="avatar", description="Retrieves an avatar")
    @app_commands.describe(user="The user who you want to see the avatar of")
    async def avatar(
        self, interaction: discord.Interaction, user: discord.Member = None
    ) -> None:
        """
        Attempts to send an embed with the user's avatar attached in the embed's image slot

        Args:
            interaction (discord.Interaction): Provided by discord, the interaction which called the command.
            user (discord.Member, optional): The user to get the avatar from. If the member is not supplied, defaults to the interaction user.

        Returns (None): Sends a discord embed as a result and returns nothing
        """
        await interaction.response.defer()  # Wait to avoid discord's 3 second command timer
        if user == None:  # if the user is not supplied by the command initiator
            user = interaction.user  # The command initiator becomes the user

        if not user.avatar:  # If the user does not have an avatar property
            embed = discord.Embed(color=blue, title="❌ Avatar Failure")
            # Create an embed and respond saying that the user does not have an avatar
            embed.description = f"@{user.name} does not have an avatar to display."
            embed.set_footer(
                text="Requested by @" + interaction.user.name,
                icon_url=interaction.user.avatar.url if interaction.user.avatar else "",
            )
            # Set the footer of the embed to reflect the command initiator
            await interaction.followup.send(embed=embed)  # Send the embed
            return  # Return from the function early

        embed = discord.Embed(title=f"✅ @{user.name}'s avatar", color=blue)
        embed.set_footer(
            text="Requested by @" + interaction.user.name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else "",
        )
        embed.set_image(url=user.avatar.url)
        # If the code has passed all guard clauses
        # Create the embed with the users avatar and send it back to the user

        await interaction.followup.send(embed=embed)  # Sends the embed to the user
        return

    @app_commands.command(name="invite", description="Invite this bot to other servers")
    async def _invite(self, interaction: discord.Interaction):
        """Sends an embed with an invite link to the discord bot
        Allows you to invite the bot to other servers

        Args:
            interaction (discord.Interaction): Provided by discord, application interaction

        Returns (None):
            Quite literally nothing
        """
        await interaction.response.defer(ephemeral=True)
        invite_url = "https://discord.com/api/oauth2/authorize?client_id=1025477778428133379&permissions=8&scope=applications.commands%20bot"
        invite_embed = discord.Embed(
            title="🎣 Invite Koi",
            color=blue,
            description=f"Thank you for being interested @{interaction.user.name}",
        )  # ^^ Create the invite embed
        temporary_view = discord.ui.View(timeout=None)
        # ^^ Creeate the view to attach the button to
        temporary_view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="Invite Koi to Your Server",
                url=invite_url,
            ),
        )  # ^^ Create the button

        await interaction.followup.send(embed=invite_embed, view=temporary_view)
        # ^^ Sending the embed along with the button
        return

    @app_commands.command(name="sync", description="This command is not for you")
    async def _sync(self, interaction: discord.Interaction) -> None:
        """An interaction command to sync all the other interaction commands

        Args:
            interaction (discord.Interaction): Provided by discord.
        """
        await interaction.response.defer(ephemeral=True)
        # ^^ Bypass 3 second discord check
        if interaction.user.id != owner_id:  # If the user of the command isn't me
            await interaction.followup.send("This command is not for you.")
            # ^^ Tell the user to leave it alone
            return  # Escape the function early

        await interaction.followup.send(
            "Syncing client tree."
        )  # Respond to the user with affirmation

    @app_commands.command(
        name="about", description="Tells you what the bot is all about"
    )
    async def _about(self, interaction: discord.Interaction) -> None:
        """An interaction command which simply tells you about the bot

        Args:
            interaction (discord.Interaction): Provided by discord.
        """

        await interaction.response.defer(ephemeral=True)
        # ^^ Bypass 3 second check from discord

        # Creating the Embed
        embed: discord.Embed = discord.Embed(title="About Me 🎣")
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.description = """**Hello! I'm Koi!**\n\nI'm here to give you a good time on discord. I also have a dedicated **Honkai: Star Rail** module.\n\nI am an open source discord bot and you can find my code [here](https://github.com/Luna-Karch/koi-bot)"""
        embed.color = blue

        await interaction.followup.send(embed=embed)
        # ^^ Sending the embed

    @app_commands.command(
        name = "display-ip", description = "Displays the IP of the local machine"
    )
    async def _display_ip(self, interaction: discord.Interaction) -> None:
        """
        An interaction command which displays the ip of the local machine, in the case that it changes due to a router restart

        Args:
            None
        """

        if interaction.user.id != 923600698967461898:
            await interaction.response.send_message("No.", ephemeral = True)
            return # If user isn't me, refuse
        
        await interaction.response.defer(ephemeral = True) # Defer until ip is displayed

        ip_stdout = subprocess.check_output("ip a | grep inet6", shell = True)
        modified_ip_stdout: str = ip_stdout.decode("utf-8") # Get IP

        await interaction.followup.send(f"```\n{modified_ip_stdout}\n```", ephemeral = True)


async def setup(client: commands.Bot) -> None:
    """
    Cog Setup Function, required for every cog that needs to be loaded.
    Adds all the commands in the cog to the client and loads them
    """
    await client.add_cog(Utilities(client))
