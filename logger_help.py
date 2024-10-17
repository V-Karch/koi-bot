# This file contains functions that are helpful for reducing code duplication
# Allows for logger to handle errors in a nicer way and drastically reduces need
# To copy and paste

import discord
from pythondebuglogger.Logger import Logger


async def defer_with_logs(
    interaction: discord.Interaction, logger: Logger, ephemeral: bool = False
) -> bool:
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
        logger.display_notice(f"[User {interaction.user.id}] is having a command defered.")
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
    message: str = None,
    embed: discord.Embed = discord.utils.MISSING,
    view: discord.ui.View = discord.utils.MISSING,
    ephemeral: bool = False,
) -> discord.Message | bool:
    """Calls `await interaction.response.send_message()`
    with the provided arguments, quality of life function to make
    logging easier

    Args:
        interaction (discord.Interaction): The interaction
        logger (Logger): The logger
        command_name (str): The name of the command the logger is in
        message (str): The message you want to send. Defaults to None
        embed (discord.Embed) The embed you want to send. Defaults to None
        view (discord.ui.View) The view you want to send. Defaults to None
        ephemeral (bool, optional): Whether it should be ephemeral or not. Defaults to False.

    Returns:
        discord.Message | False: Returns the message object if it succeeds, otherwise False
    """
    try:
        message: discord.Message = await interaction.response.send_message(
            content=message, ephemeral=ephemeral, embed=embed, view=view
        )
        logger.display_notice(
            f"[User {interaction.user.id}/{command_name}] Successfully sent reply message to [Channel {interaction.channel.id}]"
        )
        return message
    except discord.HTTPException as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] Message failed to send."
        )
        logger.display_debug(e)
        return False
    except discord.NotFound as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] This webhook was not found."
        )
        logger.display_debug(e)
        return False
    except TypeError as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] You specified both embed and embeds or file and files or thread and thread_name."
        )
        logger.display_debug(e)
        return False
    except ValueError as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] The length of embeds was invalid, there was no token associated with this webhook or ephemeral was passed with the improper webhook type or there was no state attached with this webhook when giving it a view."
        )
        logger.display_debug(e)
        return False


async def send_followup_message_with_logs(
    interaction: discord.Interaction,
    logger: Logger,
    command_name: str,
    message: str = None,
    embed: discord.Embed = discord.utils.MISSING,
    view: discord.ui.View = discord.utils.MISSING,
    ephemeral: bool = False,
) -> discord.Message | bool:
    try:
        await interaction.followup.send(
            content=message, embed=embed, view=view, ephemeral=ephemeral
        )
        logger.display_notice(
            f"[User {interaction.user.id}/{command_name}] response sent to [Channel {interaction.channel.id}]"
        )
    except discord.HTTPException as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] Message failed to send."
        )
        logger.display_debug(e)
        return False
    except discord.NotFound as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] This webhook was not found."
        )
        logger.display_debug(e)
        return False
    except TypeError as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] You specified both embed and embeds or file and files or thread and thread_name."
        )
        logger.display_debug(e)
        return False
    except ValueError as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] The length of embeds was invalid, there was no token associated with this webhook or ephemeral was passed with the improper webhook type or there was no state attached with this webhook when giving it a view."
        )
        logger.display_debug(e)
        return False
    except discord.Forbidden as e:
        logger.display_error(
            f"[User {interaction.user.id}/{command_name}] The authorization token for the webhook is incorrect."
        )
        logger.display_debug(e)
        return False
