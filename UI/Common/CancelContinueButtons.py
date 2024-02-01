from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, Interaction
from discord.ui import Button

from Assets import BotEmojis

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("CancelButton", "ContinueButton")

################################################################################
class CancelButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.danger,
            label="Cancel Posting",
            disabled=False,
            row=4
        )

    async def callback(self, interaction: Interaction):
        self.view.complete = True
        self.view._close_on_complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore

################################################################################
class ContinueButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.success,
            label="Continue",
            disabled=True,
            row=4,
            emoji=BotEmojis.ThumbsUp
        )

    async def callback(self, interaction: Interaction):
        self.view.complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore
        
################################################################################
