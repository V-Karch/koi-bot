import discord
from models.character_card_view import CharacterCardView
from typing import Dict
from pythondebuglogger.Logger import Logger
from logger_help import (
    send_followup_message_with_logs,
    defer_with_logs,
    send_response_message_with_logs,
)

logger: Logger = Logger(enable_timestamps=True)


class CharacterDropdown(discord.ui.Select):
    """Character Dropdown Menu.
    Allows the user to select one of the characters on the profile of the Honkai: Star Rail player
    """

    def __init__(
        self,
        user_id: int,
        parsed_data: Dict[str, discord.Embed] | Dict[str, Dict[str, discord.Embed]],
    ):
        logger.display_notice(
            f"[User {user_id}/hsr] started creating character dropdown"
        )
        self.user_id = user_id
        self.parsed_data = parsed_data

        options = self.make_options(parsed_data)
        super().__init__(
            placeholder="Select a character",
            max_values=1,
            min_values=1,
            options=options,
        )

    def make_options(
        self,
        parsed_data: Dict[str, discord.Embed] | Dict[str, Dict[str, discord.Embed]],
    ) -> list[discord.SelectOption]:
        """Converts the parsed data given into a list of discord select options to be added to the view

        Args:
            parsed_data (Dict[str, discord.Embed]): Information Retrieved from the Mihomo API and parsed by my parsing function in hsr.py

        Returns:
            list[discord.SelectOption]: A list of discord.SelectOption objects. Both the label and value attributes are set to the character name
        """
        logger.display_notice(f"[User {self.user_id}/hsr] calling make_options()")
        options = [
            discord.SelectOption(label=character, value=character)
            for character in parsed_data["characters"].title.split(", ")  # type: ignore
        ]

        logger.display_notice(
            f"[User {self.user_id}/hsr] finished calling make_options()"
        )
        return options

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await send_response_message_with_logs(
                interaction,
                logger,
                "hsr",
                "This interaction is not for you",
                ephemeral=True,
            )
            return

        await defer_with_logs(interaction, logger)

        character_embed = self.parsed_data["character_cards"][self.values[0]]  # type: ignore

        user_profile_picture = ""
        if interaction.user.avatar:
            user_profile_picture = interaction.user.avatar.url

        character_embed.set_footer(
            text=f"Requested by: {interaction.user.name}", icon_url=user_profile_picture
        )

        await send_followup_message_with_logs(
            interaction,
            logger,
            "hsr",
            embed=character_embed,
            view=CharacterCardView(
                interaction.user.id, self.values[0], self.parsed_data
            ),
        )
