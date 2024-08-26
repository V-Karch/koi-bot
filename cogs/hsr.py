import typing
import discord
from random import choice
from discord import app_commands
from discord.ext import commands
from mihomo.models import Character
from mihomo import Language, MihomoAPI
from mihomo.models import StarrailInfoParsed
from models.player_card_view import PlayerCardView
from mihomo.errors import InvalidParams, UserNotFound, HttpRequestError


class HSR(commands.Cog):
    """
    Honkai: Star Rail Interaction Commands Cog
    Houses all commands relating to Honkai: Star Rail
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client
        # ^^ Sets the client to be an attribute of the class
        self.hsrapi = MihomoAPI(language=Language.EN)
        # ^^ Honkai: Star Rail API Client, used for getting HSR Information
        self.FIVE_STAR_HEX = 0xFFAA4A
        self.FOUR_STAR_HEX = 0x8278ED
        self.ERROR_HEX = 0xFF5733
        # ^^ Constant variables used multiple times in the class

    async def get_hsr_data(
        self, uid: int
    ) -> StarrailInfoParsed | typing.Literal["Net"] | None:
        """Requests data from Honkai: Star Rail using a UID

        Args:
            uid (int): A user ID from Honkai: Star Rail. Ex: 613792348, 714028257

        Returns:
            StarrailInfoParsed | typing.Literal["Net"] | None:
              Returns the Honkai: Star Rail user information based on the UID if the data is retrievable.
              If there is an HttpRequestError, returns "Net"
              If there is another type of error, returns None
        """
        try:  # Attempting to get the data
            data: StarrailInfoParsed = await self.hsrapi.fetch_user(
                uid, replace_icon_name_with_url=True
            )
            return data
        except HttpRequestError:
            return "Net"
        except (InvalidParams, UserNotFound):  # If an invalid UID is passed
            return None

    def make_player_card(self, hsr_info: StarrailInfoParsed) -> discord.Embed:
        """Takes in a StarrailInfoParsed object and creates a discord Embed representing the player card.
        The player card refers to some general useful information about the player.

        This information includes Trailblaze Level, Friend Count, Equilibrium Level, Achievement Count,
        Amount of Characters Owned, and Amount of Light Cones Owned.

        Once the embed is created, returns it.

        Args:
            hsr_info (StarrailInfoParsed): The information retrieved from Mihomo's API

        Returns:
            discord.Embed: The player card embed
        """
        player_card_color = choice((self.FIVE_STAR_HEX, self.FOUR_STAR_HEX))
        player_card = discord.Embed(
            color=player_card_color,
            description="```",
        )
        player_card.set_author(
            name=hsr_info.player.name + " | " + str(hsr_info.player.uid),
            icon_url=hsr_info.player.avatar.icon,
        )

        player_attribute_mapping = {
            "Trailblaze Level": hsr_info.player.level,
            "Friends": hsr_info.player.friend_count,
            "Equilibrium Level": hsr_info.player.world_level,
            "Achievements": hsr_info.player.achievements,
            "Characters Owned": hsr_info.player.characters,
            "Light Cones Owned": hsr_info.player.light_cones,
        }

        for descriptor, value in player_attribute_mapping.items():
            player_card.description += f"{descriptor:17} -> {value:4d}\n"

        player_card.description += "```"

        return player_card

    def make_character_list(self, hsr_info: StarrailInfoParsed) -> discord.Embed:
        """Takes the hsr_info from the API and returns a list of the characters on the users profile

        Args:
            hsr_info (StarrailInfoParsed): The data from the Mihomo API

        Returns:
            discord.Embed: A discord embed whose title is a list of the characters the user has on their profile.
            To access it, simply access the embed's title property. Ex: character_list.title
        """
        character_list = discord.Embed(title="")
        character_list.title = ", ".join(
            character.name for character in hsr_info.characters
        )
        return character_list

    def calculate_total_character_stats(
        self, character: Character
    ) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
        """Returns an informational mapping of strings to attribute values that matter,
        combining them and adding the values

        Args:
            character (Character): The character object

        Returns:
            typing.Dict[str, typing.Dict[str, typing.Any]]: The stats for a character

            Example:

            {
                "HP": {"value": 3203.745155068101, "is_percent": False},
                "ATK": {"value": 3758.292158859966, "is_percent": False},
                "DEF": {"value": 882.86872982796, "is_percent": False},
                "SPD": {"value": 106.3000000002794, "is_percent": False},
                "CRIT Rate": {"value": 0.13, "is_percent": True},
                "CRIT DMG": {"value": 0.74624000582844, "is_percent": True},
                "Effect Hit Rate": {"value": 0.40672000464983693, "is_percent": True},
                "Break Effect": {"value": 0.28, "is_percent": True},
                "Effect RES": {"value": 0.22896000347100504, "is_percent": True},
                "Lightning DMG Boost": {"value": 0.1, "is_percent": True},
            }
        """

        raw_stats = character.attributes + character.additions
        # ^^ Getting the raw value of all the attributes

        total_stats: typing.Dict[str, typing.Dict[str, typing.Any]] = {}

        for attribute in raw_stats:
            if not total_stats.get(attribute.name):
                # ^^ If the key does not already exist in the dictionary
                total_stats[attribute.name] = {
                    "value": attribute.value,
                    "is_percent": attribute.is_percent,
                }  # Create the value in the dictionary
            else:  # If the key already does exist
                total_stats[attribute.name]["value"] += attribute.value
                # ^^ Add the values together

        return total_stats

    def make_character_cards(
        self, hsr_info: StarrailInfoParsed
    ) -> typing.Dict[str, discord.Embed]:
        """Creates a dictionary of character names mapped to character cards, which are discord Embeds
        Each card will contain important information about each character

        Args:
            hsr_info (StarrailInfoParsed): Parsed Honkai: Star Rail Info parsed from Mihomo's API

        Returns:
            typing.Dict[str, discord.Embed]: {character_name (str): character_card (discord.Embed)}
        """
        character_cards: typing.Dict[str, discord.Embed] = {}
        # ^^ The initial Empty dictionary to be returned

        for character in hsr_info.characters:  # For every character available
            element_color = int("0x" + character.element.color[1:], 0)  # Get hex code
            character_stats = self.calculate_total_character_stats(character)
            # ^^  Calculate the characters total stats

            character_card: discord.Embed = discord.Embed(
                description="```diff\n",
                color=element_color,
            )  # Create the Embed

            for stat in character_stats:
                character_card.description += (
                    f"+ {stat:28}-> {int(character_stats[stat]['value']):8}\n"
                    if not character_stats[stat]["is_percent"]
                    else f"+ {stat:28}-> {round((character_stats[stat]['value'] * 100), 1):7}%\n"
                )
                # ^^ String formatting, adding in the stats to the codeblock

            character_card.description += "```"

            character_card.set_author(
                name=f"{character.name} - Lvl {character.level}/{character.max_level} -  E{character.eidolon}",
                icon_url=character.icon,
            )

            character_card.set_image(url=character.preview)
            character_cards[character.name] = character_card
            # ^^ Add the character card to the dictionary

        return character_cards

    def make_lightcone_cards(
        self, hsr_info: StarrailInfoParsed
    ) -> typing.Dict[str, discord.Embed]:
        """Creates a dictionary of strings mapped to discord embed, which is just the character mapped to their lightcone
        but in a nice fancy embed.

        Args:
            hsr_info (StarrailInfoParsed): Data parsed from mihomo api

        Returns:
            typing.Dict[str, discord.Embed]: A mapping of character names to embeds
            {"Kafka": discord.Embed(), ...}
        """

        lightcone_cards: typing.Dict[str, discord.Embed] = {}

        for character in hsr_info.characters:
            if character.light_cone is None:
                lightcone_cards[character.name] = discord.Embed(title = "No Lightcone :(", color=0xff0000)
                break # If there is no lightcone, exit loop

            lightcone_name = f" {character.light_cone.name}"
            lightcone_name += f" - Lvl {character.light_cone.level} / {character.light_cone.max_level}"
            lightcone_color = int("0x" + character.element.color[1:], 0)

            lightcone_embed = discord.Embed(
                title=lightcone_name, color=lightcone_color, description="```diff\n"
            )

            for attribute in character.light_cone.attributes:
                if not attribute.is_percent:
                    lightcone_embed.description += (
                        f"+ {attribute.name:15} -> {int(attribute.displayed_value):8}\n"
                    )
                else:
                    lightcone_embed.description += f"+ {attribute.name:15} -> {round((attribute.value * 100), 1):7}%\n"

            for _property in character.light_cone.properties:
                if not _property.is_percent:
                    lightcone_embed.description += (
                        f"+ {_property.name:15} -> {int(_property.displayed_value):8}\n"
                    )
                else:
                    lightcone_embed.description += f"+ {_property.name:15} -> {round((_property.value * 100), 1):7}%\n"

            lightcone_embed.description += "```"

            lightcone_embed.set_image(url=character.light_cone.portrait)

            lightcone_embed.set_footer(
                text=f"{character.name}'s Lightcone", icon_url=character.icon
            )

            lightcone_cards[character.name] = lightcone_embed

        return lightcone_cards

    def parse_data(
        self, hsr_info: StarrailInfoParsed
    ) -> typing.Dict[str, discord.Embed | typing.Dict[str, discord.Embed]]:
        player_card = self.make_player_card(hsr_info)
        character_list = self.make_character_list(hsr_info)
        character_cards = self.make_character_cards(hsr_info)
        lightcone_cards = self.make_lightcone_cards(hsr_info)
        # ^^ Creating all the data

        resulting_dictionary = {
            "player_card": player_card,
            "characters": character_list,
            "character_cards": character_cards,
            "lightcone_cards": lightcone_cards,
        }  # ^^ Formatting it nicely
        return resulting_dictionary  # Returning the nice data

    @app_commands.command(
        name="hsr",
        description="Get information about a Honkai: Star Rail player from their UID",
    )
    @app_commands.describe(
        uid="The Honkai: Star Rail UID of the user you want the information on"
    )
    async def hsr(self, interaction: discord.Interaction, uid: int):
        await interaction.response.defer()  # Bypass the 3 second timeout since this function requires an api call
        data = await self.get_hsr_data(uid)

        if isinstance(data, str):  # If an HttpRequestError occurs
            embed: discord.Embed = discord.Embed(
                color=self.ERROR_HEX,
                title="Whoops!",
                description="Something is wrong with the API service right now. It must be down for an update or something of the sort",
            )
            await interaction.followup.send(embed=embed)
            return  # Quitting the function early

        if data == None:  # If the request failed due to invalid parameters
            embed: discord.Embed = discord.Embed(
                color=self.ERROR_HEX,
                title="Whoops!",
                description="Either you provided an invalid input number or the user could not be found in the database.",
            )
            await interaction.followup.send(embed=embed)
            return  # Quitting the function early

        parsed_data = self.parse_data(data)  # Parsing the retrieved data

        await interaction.followup.send(
            embed=parsed_data["player_card"],
            view=PlayerCardView(interaction.user.id, parsed_data),
        )  # For now, just send the player card


async def setup(client: commands.Bot) -> None:
    """Cog Setup Function, required for every cog that needs to be loaded.
    Adds all the commands in the cog to the client and loads them"""
    await client.add_cog(HSR(client))
