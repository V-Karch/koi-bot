import discord
from typing import Dict
from models.character_dropdown import CharacterDropdown


class PlayerCardView(discord.ui.View):
    def __init__(
        self,
        user_id: int,
        parsed_data: Dict[str, discord.Embed] | Dict[str, Dict[str, discord.Embed]],
    ):
        """This is the view used to hold the dropdown menu for each character and is sent when /hsr is run

        Args:
            user_id (int): The user's ID, this will be used in the selection dropdown to determine if the user is allowed to interact with it or not
            parsed_data (Dict[str, discord.Embed]): The data I parsed from Mihomo's API in hsr.py
        """
        self.user_id = user_id
        self.parsed_data = parsed_data

        super().__init__(timeout=None)
        self.add_item(CharacterDropdown(user_id, parsed_data))
