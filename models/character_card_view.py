import typing
import discord


class CharacterCardView(discord.ui.View):
    def __init__(
        self,
        user_id: int,
        character: str,
        parsed_data: typing.Dict[str, discord.Embed]
        | typing.Dict[str, typing.Dict[str, discord.Embed]],
    ):
        self.user_id = user_id
        self.character = character
        self.parsed_data = parsed_data
        super().__init__(timeout=None)

    @discord.ui.button(label="Lightcone", style=discord.ButtonStyle.blurple, emoji="🃏")
    async def lightcone_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        button.disabled = True
        await interaction.followup.edit_message(interaction.message.id, view=self)
        await interaction.followup.send(
            embed=self.parsed_data["lightcone_cards"][self.character]
        )
