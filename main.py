import os
import typing
import discord
from discord.ext import commands
from pythondebuglogger.Logger import Logger

logger: Logger = Logger(enable_timestamps=True)
logger.display_notice("Debug Logger Initialized")

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
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            token: str = f.read()
            
        return token.strip()
    except Exception as exception:
        logger.display_error("Failed to read token.txt when calling load_token() in main.py")
        exit(1) # Exit with code 1 if token can't be read
        
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
            logger.display_error(f"Color value cannot be out of range 0-255.\n Values given: {rgb}")
            exit(1) # # Tells the user they messed up and explains how

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
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                logger.display_notice(f"Cog {filename} successfully loaded")
            except Exception as exception:
                logger.display_error(f"Cog {filename }failed to load")

client = commands.Bot(**SETUP_KWARGS)
logger.display_notice("discord.commands.Bot Object created successfully")


@client.command(name="sync")
async def _sync(ctx: commands.Context):
    if ctx.author.id != OWNER_ID:
        logger.display_error(f"User with ID {ctx.user.id} attempted to sync command tree.")
        return

    logger.display_notice("Starting command tree sync")
    await client.tree.sync()
    await ctx.send("Syncing...")
    logger.display_notice("Command tree sync has successfully been requested from discord")


@client.event
async def on_ready() -> None:
    """This function runs when the client is "ready"
    It's current purpose is simply to notify the person running the program that
    the program is running without errors and is connected to discord"""
    logger.display_notice("Starting cog loader")
    await load_cogs(client)
    logger.display_notice("Attempted to load all cogs")
    cprint(STARTUP_ART, BLUE)
    logger.display_notice("The bot is now running successfully")


client.run(load_token())
