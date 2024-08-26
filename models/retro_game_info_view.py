import discord
from discord.ext import commands

blue = 0x73BCF8 # Hex color blue stored for embed usage

class RetroGameInfoView(discord.ui.View):
    def __init__(self, dict_game_info_and_progress_stdout: dict, timeout = None):
        self.dict_game_info_and_progress_stdout = dict_game_info_and_progress_stdout
        super().__init__(timeout = timeout)

    @discord.ui.button(label = "Game Information", style = discord.ButtonStyle.blurple, emoji = "🎮")
    async def callback(self, interaction: discord.Interaction, button: discord.Button):
        message_id: int = interaction.message.id
        await interaction.response.defer()

        # Setup Variables
        game_title: str = self.dict_game_info_and_progress_stdout.get("title")
        game_icon: str = "https://media.retroachievements.org" + self.dict_game_info_and_progress_stdout.get("imageIcon")
        game_developer: str = self.dict_game_info_and_progress_stdout.get("developer")
        game_publisher: str = self.dict_game_info_and_progress_stdout.get("publisher")
        game_genre: str = self.dict_game_info_and_progress_stdout.get("genre")
        game_release_date: str = self.dict_game_info_and_progress_stdout.get("released")
        game_console: str = self.dict_game_info_and_progress_stdout.get("consoleName")

        game_achievement_count: int = self.dict_game_info_and_progress_stdout.get("numAchievements")
        user_unlocked_softcore: int = self.dict_game_info_and_progress_stdout.get("numAwardedToUser")
        user_unlocked_hardcore: int = self.dict_game_info_and_progress_stdout.get("numAwardedToUserHardcore")
        
        user_completion_softcore: str = self.dict_game_info_and_progress_stdout.get("userCompletion")
        user_completion_hardcore: str = self.dict_game_info_and_progress_stdout.get("userCompletionHardcore")

        # Construct Embed
        output_embed: discord.Embed = discord.Embed(title = game_title, color = blue, description = "")
        output_embed.set_thumbnail(url = game_icon)
        output_embed.description += f"**Developer: {game_developer}**\n"
        output_embed.description += f"**Publisher: {game_publisher}**\n"
        output_embed.description += f"**Genre: {game_genre}**\n"
        output_embed.description += f"**Released: {game_release_date}**\n"
        output_embed.description += f"**Console: {game_console}**\n"

        output_embed.description += "\n**Achievement Stats:**\n"
        output_embed.description += f"**Softcore: {user_unlocked_softcore}/{game_achievement_count} ({user_completion_softcore})**\n"
        output_embed.description += f"**Hardcore: {user_unlocked_hardcore}/{game_achievement_count} ({user_completion_hardcore})**\n"

        button.disabled = True # Disable the button after it is clicked

        # Respond To User
        await interaction.followup.send(embed = output_embed)
        await interaction.followup.edit_message(message_id, view = self)
