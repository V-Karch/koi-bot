# This file contains functions that are helpful for reducing code duplication
# Allows for logger to handle errors in a nicer way and drastically reduces need
# To copy and paste

import discord
from pythondebuglogger.Logger import Logger


async def defer_with_logs(
    interaction: discord.Interaction, logger: Logger, ephemeral: bool = False
):
    """This function called interaction.response.defer() with the provided arguments.
    It will allow for easier dealing with logs and errors

    Args:
        interaction (discord.Interaction): The discord interaction
        logger (Logger): The logger object
        ephemeral (bool, optional): True or False, Ephemeral or not. Defaults to False.

    Returns:
        bool: True if the defer was successful, False otherwise
    """

    try:
        await interaction.response.defer(ephemeral=ephemeral)
        logger.display_notice(f"[{interaction.user.id}] is having a command defered.")
        return True
    except discord.HTTPException:
        logger.display_error(f"[Interaction {interaction.id}] failed to defer.")
        return False
    except discord.InteractionResponded:
        logger.display_error(
            f"[Interaction {interaction.id}] has already been responded to."
        )
        return False


async def send_response_message_with_logs(
    interaction: discord.Interaction,
    logger: Logger,
    command_name: str,
    message: str,
    ephemeral: bool = False,
):
    try:
        message: discord.Message = await interaction.response.send_message(
            message, ephemeral=ephemeral
        )
        logger.display_notice(
            f"[User {interaction.user.id}/{command_name}] Successfully sent reply message to [Channel {interaction.channel.id}]"
        )
        return message
    except discord.HTTPException:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] Message failed to send."
        )
        return False
    except discord.NotFound:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] This webhook was not found."
        )
        return False
    except TypeError:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] You specified both embed and embeds or file and files or thread and thread_name."
        )
        return False
    except ValueError:
        logger.display_error(
            f"User {interaction.user.id}/{command_name} The length of embeds was invalid, there was no token associated with this webhook or ephemeral was passed with the improper webhook type or there was no state attached with this webhook when giving it a view."
        )
        return False
