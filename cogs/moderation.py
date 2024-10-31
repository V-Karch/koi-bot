import discord
from discord import app_commands
from discord.ext import commands
from pythondebuglogger.Logger import Logger
from logger_help import defer_with_logs, send_followup_message_with_logs

logger: Logger = Logger(enable_timestamps=True)


class Moderation(commands.Cog):
    """
    A Discord cog for moderation commands.

    Attributes:
        client (commands.Bot): The bot client that this cog is added to.
    """

    def __init__(self, client: commands.Bot):
        """
        Initializes the Moderation cog with the bot client.

        Args:
            client (commands.Bot): The bot instance to which this cog is attached.
        """
        self.client = client

    @app_commands.command(name="kick", description="Kicks a user from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """
        Kicks a specified member from the server, provided the command user has kick permissions.

        Logs the command initiation, defers the interaction, and attempts to kick the member.
        Sends a success message if the operation is successful or an error message if permissions
        are insufficient.

        Args:
            interaction (discord.Interaction): The interaction that triggered this command.
            member (discord.Member): The member to be kicked from the server.
            reason (str): The reason for the kick, defaults to "No reason provided."

        Raises:
            discord.Forbidden: If the bot does not have permission to kick the user.
        """
        logger.display_notice(f"[User {interaction.user.id}] is running /kick")
        await defer_with_logs(interaction, logger)

        try:
            logger.display_notice(
                f"[User {interaction.user.id}/kick] is attempting to kick [User {member.id}]"
            )
            await member.kick(reason=reason)
            await send_followup_message_with_logs(
                interaction,
                logger,
                "kick-success",
                f"{member.display_name} has been kicked from the server for: {reason}",
            )
            logger.display_notice(
                f"[User {interaction.user.id}/kick] successfully kicked [User {member.id}]"
            )
        except discord.Forbidden:
            await send_followup_message_with_logs(
                interaction,
                logger,
                "kick-fail-no-permissions",
                "I couldn't kick this user due to lack of permissions.",
            )
            logger.display_error(
                f"[User {interaction.user.id}/kick] Failed to execute command"
            )


async def setup(client: commands.Bot):
    """
    Sets up the Moderation cog for the specified bot client.

    This function is an entry point for loading the cog, enabling the bot to register
    and use the moderation commands provided in this cog.

    Args:
        client (commands.Bot): The bot instance to which the Moderation cog is added.
    """
    await client.add_cog(Moderation(client))
