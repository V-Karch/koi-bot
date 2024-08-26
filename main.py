import os
import typing
import discord
from discord.ext import commands


OWNER_ID = 923600698967461898  # My user ID if someone is cloning this bot from github, this must be changed

SETUP_KWARGS: dict[str, typing.Any] = {
    "intents": discord.Intents.all(),  # What the bot intends to use
    "command_prefix": "~",  # The command prefix
    "help_command": None,  # Removing the default help command
    "description": "A cute, general purpose discord bot",  # bot description
}  # Bot setup keyword arguments

BLUE = (155, 188, 248)
# ^^ RGB values for the color blue

STARTUP_ART: str = """
╔═══════════════════════════════════════════════════════════════════════╗
║ █████   ████           ███             ███████████            █████   ║
║░░███   ███░           ░░░             ░░███░░░░░███          ░░███    ║
║ ░███  ███     ██████  ████             ░███    ░███  ██████  ███████  ║
║ ░███████     ███░░███░░███  ██████████ ░██████████  ███░░███░░░███░   ║
║ ░███░░███   ░███ ░███ ░███ ░░░░░░░░░░  ░███░░░░░███░███ ░███  ░███    ║
║ ░███ ░░███  ░███ ░███ ░███             ░███    ░███░███ ░███  ░███ ███║
║ █████ ░░████░░██████  █████            ███████████ ░░██████   ░░█████ ║
║░░░░░   ░░░░  ░░░░░░  ░░░░░            ░░░░░░░░░░░   ░░░░░░     ░░░░░  ║
╚═══════════════════════════════════════════════════════════════════════╝
"""


def load_token() -> str:
    """
    Loads the bot's authorization token from the token file
    Args: None
    Returns (str): The bot's authorization token
    """
    with open("token.txt", "r", encoding="utf-8") as f:
        token: str = f.read()

    return token.strip()


def cprint(text: str, rgb: tuple[int]) -> None:
    """Prints text in any color provided RGB values

    Args:
        text (str): The text you want to print in rgb
        rgb (tuple[int]): RGB format of the color value you want to print the text with

    Returns (None): Prints a statement

    Raises:
        IndexError: If the color values are outside the RGB spectrum, if any value is outside the range 0 <= r, g, b <= 255
    """

    for color_value in rgb:
        if not (0 <= color_value <= 255):
            raise IndexError(
                f"Color value cannot be out of range 0-255.\n Values given: {rgb}"
            )  # Tells the user they messed up and explains how

    output_template: str = "\033[38;2;red;green;bluem{text}\033[0m"
    # ^^ Template string, replaces values red, green, blue, and text accordingly
    print(
        output_template.replace("red", str(rgb[0]))
        .replace("green", str(rgb[1]))
        .replace("blue", str(rgb[2]))
        .replace("{text}", text)
    )  # Printing the replace output


async def load_cogs(client: commands.Bot) -> None:
    """
    Loads all the cogs from the cogs folder
    and connects them to the discord bot

    Args:
        client (commands.Bot): The discord bot object

    Returns (None): There is nothing to return
    """

    for filename in os.listdir("cogs"):  # for every cog in the cogs folder
        if filename[-1] == "y":
            # ^^ If the cog ends in "y", checking if it's a python file
            await client.load_extension(f"cogs.{filename[:-3]}")
            cprint(f"[+] loaded {filename}", BLUE)
            # ^^ Load the cog into the bot


client = commands.Bot(**SETUP_KWARGS)


@client.command(name="sync")
async def _sync(ctx: commands.Context):
    if ctx.author.id != OWNER_ID:
        return

    await client.tree.sync()
    await ctx.send("Syncing...")


@client.event
async def on_ready() -> None:
    """This function runs when the client is "ready"
    It's current purpose is simply to notify the person running the program that
    the program is running without errors and is connected to discord"""
    await load_cogs(client)
    cprint(STARTUP_ART, BLUE)
    cprint(f"Is now running...", BLUE)


client.run(load_token())
