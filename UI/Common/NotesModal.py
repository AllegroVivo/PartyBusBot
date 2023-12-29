from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("NotesModal",)

################################################################################
class NotesModal(FroggeModal):

    def __init__(self, cur_val: str):

        super().__init__(title="Edit Individual Notes")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter notes for this individual...",
                value="Enter notes for this individual...",
                required=False
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Notes",
                placeholder="eg. 'Allegro is the best~!'",
                value=cur_val,
                max_length=2000,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################
