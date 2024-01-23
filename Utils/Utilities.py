import math
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

from discord import Colour, Embed, EmbedField

from .Enums import Hours, Timezone
from Utils.Colors import CustomColor
################################################################################

__all__ = ("Utilities", )

################################################################################
class Utilities:

    @staticmethod
    def make_embed(
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Union[Colour, int]] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        author_text: Optional[str] = None,
        author_url: Optional[str] = None,
        author_icon: Optional[str] = None,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        timestamp: Union[datetime, bool] = False,
        fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None
    ) -> Embed:
        """Creates and returns a Discord embed with the provided parameters.
    
        All parameters are optional.
    
        Parameters:
        -----------
        title: :class:`str`
            The embed's title.
    
        description: :class:`str`
            The main text body of the embed.
    
        url: :class:`str`
            The URL for the embed title to link to.
    
        color: Optional[Union[:class:`Colour`, :class:`int`]]
            The desired accent color. Defaults to :func:`colors.random_all()`
    
        thumbnail_url: :class:`str`
            The URL for the embed's desired thumbnail image.
    
        image_url: :class:`str`
            The URL for the embed's desired main image.
    
        footer_text: :class:`str`
            The text to display at the bottom of the embed.
    
        footer_icon: :class:`str`
            The icon to display to the left of the footer text.
    
        author_name: :class:`str`
            The text to display at the top of the embed.
    
        author_url: :class:`str`
            The URL for the author text to link to.
    
        author_icon: :class:`str`
            The icon that appears to the left of the author text.
    
        timestamp: Union[:class:`datetime`, `bool`]
            Whether to add the current time to the bottom of the embed.
            Defaults to ``False``.
    
        fields: Optional[List[Union[Tuple[:class:`str`, Any, :class:`bool`], :class:`EmbedField`]]]
            List of tuples or EmbedFields, each denoting a field to be added
            to the embed. If entry is a tuple, values are as follows:
                0 -> Name | 1 -> Value | 2 -> Inline (bool)
            Note that in the event of a tuple, the value at index one is automatically cast to a string for you.
    
        Returns:
        --------
        :class:`Embed`
            The finished embed object.
    
        """

        embed = Embed(
            colour=color if color is not None else CustomColor.random_all(),
            title=title,
            description=description,
            url=url
        )

        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)

        if author_text is not None:
            embed.set_author(
                name=author_text,
                url=author_url,
                icon_url=author_icon
            )

        if footer_text is not None:
            embed.set_footer(
                text=footer_text,
                icon_url=footer_icon
            )

        if isinstance(timestamp, datetime):
            embed.timestamp = timestamp
        elif timestamp is True:
            embed.timestamp = datetime.now()

        if fields is not None:
            if all(isinstance(f, EmbedField) for f in fields):
                embed.fields = fields
            else:
                for f in fields:
                    if isinstance(f, EmbedField):
                        embed.fields.append(f)
                    elif isinstance(f, tuple):
                        embed.add_field(name=f[0], value=f[1], inline=f[2])
                    else:
                        continue

        return embed

################################################################################
    @staticmethod
    def _text_length(text: str) -> float:

        value = 0.0

        for c in text:
            if c == "'":
                value += 0.25
            elif c in ("i", "j", ".", " "):
                value += 0.30
            elif c in ("I", "!", ";", "|", ","):
                value += 0.35
            elif c in ("f", "l", "`", "[", "]"):
                value += 0.40
            elif c in ("(", ")", "t"):
                value += 0.45
            elif c in ("r", "t", "1" "{", "}", '"', "\\", "/"):
                value += 0.50
            elif c in ("s", "z", "*", "-"):
                value += 0.60
            elif c in ("x", "^"):
                value += 0.65
            elif c in ("a", "c", "e", "g", "k", "v", "y", "J", "7", "_", "=", "+", "~", "<", ">", "?"):
                value += 0.70
            elif c in ("n", "o", "u", "2", "5", "6", "8", "9"):
                value += 0.75
            elif c in ("b", "d", "h", "p", "q", "E", "F", "L", "S", "T", "Z", "3", "4", "$"):
                value += 0.80
            elif c in ("P", "V", "X", "Y", "0"):
                value += 0.85
            elif c in ("A", "B", "C", "D", "K", "R", "#", "&"):
                value += 0.90
            elif c in ("G", "H", "U"):
                value += 0.95
            elif c in ("w", "N", "O", "Q", "%"):
                value += 1.0
            elif c in ("m", "W"):
                value += 1.15
            elif c == "M":
                value += 1.2
            elif c == "@":
                value += 1.3

        return value

################################################################################
    @staticmethod
    def draw_line(*, text: str = "", num_emoji: int = 0, extra: float = 0.0) -> str:

        text_value = extra + (1.95 * num_emoji) + Utilities._text_length(text)
        return "═" * math.ceil(text_value)

################################################################################
    @staticmethod
    def wrap_text(text: str, max_chars: int) -> str:

        words = text.split()
        ret = ""
        line = ""

        for word in words:
            if len(line) + len(word) + 1 > max_chars:
                ret += line.strip() + "\n"
                line = ""
            line += word + " "

        ret += line.strip()  # Add the last line

        return ret

################################################################################
    @staticmethod
    def try_parse_int(text: str) -> Optional[int]:

        try:
            return int(text)
        except ValueError:
            pass

        try:
            if "/" in text:
                split = text.split("/")
                return int(split[0])
        except ValueError:
            return None

################################################################################
    @staticmethod
    def shift_time(time: Hours, tz: Timezone) -> Hours:
        
        pass
    
################################################################################
