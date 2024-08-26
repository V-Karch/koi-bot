import discord
from models.character_card_view import CharacterCardView
from typing import Dict


class CharacterDropdown(discord.ui.Select):
    """Character Dropdown Menu.
    Allows the user to select one of the characters on the profile of the Honkai: Star Rail player
    """

    def __init__(
        self,
        user_id: int,
        parsed_data: Dict[str, discord.Embed] | Dict[str, Dict[str, discord.Embed]],
    ):
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
        options = [
            discord.SelectOption(label=character, value=character)
            for character in parsed_data["characters"].title.split(", ")
        ]

        return options

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This interaction is not for you", ephemeral=True
            )
            return

        await interaction.response.defer()

        character_embed = self.parsed_data["character_cards"][self.values[0]]

        user_profile_picture = ""
        if interaction.user.avatar:
            user_profile_picture = interaction.user.avatar.url

        character_embed.set_footer(
            text=f"Requested by: {interaction.user.name}", icon_url=user_profile_picture
        )

        await interaction.followup.send(
            embed=character_embed,
            view=CharacterCardView(
                interaction.user.id, self.values[0], self.parsed_data
            ),
        )
