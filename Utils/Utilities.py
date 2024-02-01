import math
import re
from datetime import datetime, date, time
from typing import Any, List, Optional, Tuple, Union, Literal

from discord import Colour, Embed, EmbedField

from Utils.Colors import CustomColor
from .Enums import Hours, Timezone

################################################################################

__all__ = ("Utilities", )

TimestampStyle = Literal["f", "F", "d", "D", "t", "T", "R"]

################################################################################
class Utilities:

    TIMEZONE_OFFSETS = {
        Timezone.MIT: -11,  # Midway Islands Time
        Timezone.HST: -10,  # Hawaii Standard Time
        Timezone.AST: -9,   # Alaska Standard Time
        Timezone.PST: -8,   # Pacific Standard Time
        Timezone.MST: -7,   # Mountain Standard Time
        Timezone.CST: -6,   # Central Standard Time
        Timezone.EST: -5,   # Eastern Standard Time
        Timezone.PRT: -4,   # Puerto Rico and US Virgin Islands Time
        Timezone.AGT: -3,   # Argentina Standard Time
        Timezone.CAT: -2,   # Central African Time
        Timezone.GMT: 0,    # Greenwich Mean Time
        Timezone.ECT: 1,    # European Central Time
        Timezone.EET: 2,    # Eastern European Time
        Timezone.EAT: 3,    # Eastern African Time
        Timezone.NET: 4,    # Near East Time
        Timezone.PLT: 5,    # Pakistan Lahore Time
        Timezone.BST: 6,    # Bangladesh Standard Time
        Timezone.VST: 7,    # Vietnam Standard Time
        Timezone.CTT: 8,    # China Taiwan Time
        Timezone.JST: 9,    # Japan Standard Time
        Timezone.AET: 10,   # Australian Eastern Time
        Timezone.SST: 11,   # Solomon Standard Time
        Timezone.NST: 12,   # New Zealand Standard Time
        # Note: Null timezone is omitted
    }
    
################################################################################
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
    def titleize(text: str) -> str:

        return re.sub(
            r"[A-Za-z]+('[A-Za-z]+)?",
            lambda word: word.group(0).capitalize(),
            text
        )
    
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
    def shift_time(_time: time, tz: Timezone) -> time:

        hour = _time.hour
        tz_offset = Utilities.TIMEZONE_OFFSETS.get(tz)
        utc_value = hour  # - tz_offset

        if utc_value >= 24:
            utc_value -= 24
        elif utc_value < 0:
            utc_value += 24

        return time(hour=utc_value, minute=_time.minute, second=_time.second)
    
################################################################################
    @staticmethod
    def time_to_datetime(_time: time) -> datetime:
        
        return datetime(
            year=2069, 
            month=4, 
            day=20, 
            hour=_time.hour,
            minute=_time.minute, 
            second=_time.second
        )
    
################################################################################
    @staticmethod
    def date_to_datetime(_date: date) -> datetime:
        
        return datetime(
            year=_date.year, 
            month=_date.month, 
            day=_date.day, 
            hour=0,
            minute=0, 
            second=0
        )
    
################################################################################
    @staticmethod
    def format_dt(dt: datetime, /, style: TimestampStyle | None = None) -> str:
        """A helper function to format a :class:`datetime.datetime` for presentation within Discord.

        This allows for a locale-independent way of presenting data using Discord specific Markdown.

        +-------------+----------------------------+-----------------+
        |    Style    |       Example Output       |   Description   |
        +=============+============================+=================+
        | t           | 22:57                      | Short Time      |
        +-------------+----------------------------+-----------------+
        | T           | 22:57:58                   | Long Time       |
        +-------------+----------------------------+-----------------+
        | d           | 17/05/2016                 | Short Date      |
        +-------------+----------------------------+-----------------+
        | D           | 17 May 2016                | Long Date       |
        +-------------+----------------------------+-----------------+
        | f (default) | 17 May 2016 22:57          | Short Date Time |
        +-------------+----------------------------+-----------------+
        | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
        +-------------+----------------------------+-----------------+
        | R           | 5 years ago                | Relative Time   |
        +-------------+----------------------------+-----------------+

        Note that the exact output depends on the user's locale setting in the client. The example output
        presented is using the ``en-GB`` locale.

        Parameters
        ----------
        dt: :class:`datetime.datetime`
            The datetime to format.
        style: :class:`str`
            The style to format the datetime with.

        Returns
        -------
        :class:`str`
            The formatted string.
        """
        if style is None:
            return f"<t:{int(dt.timestamp())}>"
        return f"<t:{int(dt.timestamp())}:{style}>"
    
################################################################################
