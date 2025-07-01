import typing
import discord
from pythondebuglogger.Logger import Logger
from logger_help import defer_with_logs, send_followup_message_with_logs

logger: Logger = Logger(enable_timestamps=True)


class CharacterCardView(discord.ui.View):
    def __init__(
        self,
        user_id: int,
        character: str,
        parsed_data: (
            typing.Dict[str, discord.Embed]
            | typing.Dict[str, typing.Dict[str, discord.Embed]]
        ),
    ):
        logger.display_notice(
            f"[User {user_id}/hsr] creating character card view for `{character}`"
        )

        self.user_id = user_id
        self.character = character
        self.parsed_data = parsed_data
        super().__init__(timeout=None)

    @discord.ui.button(label="Lightcone", style=discord.ButtonStyle.blurple, emoji="🃏")
    async def lightcone_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await defer_with_logs(interaction, logger)
        button.disabled = True

        try:
            await interaction.followup.edit_message(interaction.message.id, view=self)  # type: ignore
        except discord.HTTPException:
            logger.display_error(
                f"[User {self.user_id}/hsr] command failed due to an HTTPException"
            )
        except discord.Forbidden:  # type: ignore
            logger.display_error(
                f"[User {self.user_id}/hsr] cannot edit a message you did not send"
            )
        except TypeError:
            logger.display_error(
                f"[User {self.user_id}/hsr] you specified both embed and embeds"
            )
        except ValueError:
            logger.display_error(
                f"[User {self.user_id}/hsr] invalid length of embeds parameter"
            )

        await send_followup_message_with_logs(
            interaction,
            logger,
            "hsr/lightcone_button",
            embed=self.parsed_data["lightcone_cards"][self.character],  # type: ignore
        )
