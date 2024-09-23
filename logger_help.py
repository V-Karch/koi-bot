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
