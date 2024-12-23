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
    @app_commands.describe(
        member="The member you want to kick", reason="The reason for kicking the member"
    )
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

    @app_commands.command(name="ban", description="Bans a user from the server")
    @app_commands.describe(
        member="The member you want to ban", reason="The reason for banning the member"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        """
        Bans a specified member from the server, provided the command user has ban permissions.

        Logs the command initiation, defers the interaction, and attempts to ban the member.
        Sends a success message if the operation is successful or an error message if permissions
        are insufficient.

        Args:
            interaction (discord.Interaction): The interaction that triggered this command.
            member (discord.Member): The member to be banned from the server.
            reason (str): The reason for the ban, defaults to "No reason provided."

        Raises:
            discord.Forbidden: If the bot does not have permission to ban the user.
        """
        logger.display_notice(f"[User {interaction.user.id}] is running /ban")
        await defer_with_logs(interaction, logger)

        try:
            logger.display_notice(
                f"[User {interaction.user.id}/ban] is attempting to ban [User {member.id}]"
            )
            await member.ban(reason=reason)
            await send_followup_message_with_logs(
                interaction,
                logger,
                "ban-success",
                f"{member.display_name} has been banned from the server for: {reason}",
            )
            logger.display_notice(
                f"[User {interaction.user.id}/ban] successfully banned [User {member.id}]"
            )
        except discord.Forbidden:
            await send_followup_message_with_logs(
                interaction,
                logger,
                "ban-fail-no-permissions",
                "I couldn't ban this user due to lack of permissions.",
            )
            logger.display_error(
                f"[User {interaction.user.id}/ban] Failed to execute command"
            )

    @app_commands.command(name="role", description="Assigns a role to a user")
    @app_commands.describe(
        member="The member to whom you want to assign the role",
        role="The role you want to assign to the member",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
    ):
        """
        Assigns a specified role to a member, provided the command user has manage roles permissions.

        Logs the command initiation, defers the interaction, and attempts to assign the role.
        Sends a success message if the operation is successful or an error message if permissions
        are insufficient or if the role is above the bot's highest role.

        Args:
            interaction (discord.Interaction): The interaction that triggered this command.
            member (discord.Member): The member to whom the role will be assigned.
            role (discord.Role): The role to be assigned to the member.

        Raises:
            discord.Forbidden: If the bot does not have permission to manage roles.
        """
        logger.display_notice(f"[User {interaction.user.id}] is running /role")
        await defer_with_logs(interaction, logger)

        try:
            logger.display_notice(
                f"[User {interaction.user.id}/role] is attempting to assign [Role {role.id}] to [User {member.id}]"
            )

            # Check if the bot's highest role is above the role to be assigned
            if role >= interaction.guild.me.top_role:
                await send_followup_message_with_logs(
                    interaction,
                    logger,
                    "role-fail-high-role",
                    "I can't assign this role as it is higher than my highest role.",
                )
                logger.display_error(
                    f"[User {interaction.user.id}/role] Failed: [Role {role.id}] is higher than bot's highest role"
                )
                return

            await member.add_roles(
                role, reason=f"Role assigned by {interaction.user.display_name}"
            )
            await send_followup_message_with_logs(
                interaction,
                logger,
                "role-success",
                f"{member.display_name} has been assigned the role {role.name} successfully.",
            )
            logger.display_notice(
                f"[User {interaction.user.id}/role] successfully assigned [Role {role.id}] to [User {member.id}]"
            )
        except discord.Forbidden:
            await send_followup_message_with_logs(
                interaction,
                logger,
                "role-fail-no-permissions",
                "I couldn't assign the role due to lack of permissions.",
            )
            logger.display_error(
                f"[User {interaction.user.id}/role] Failed to execute command due to permissions"
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
