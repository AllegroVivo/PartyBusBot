from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("VenueNameModal",)

################################################################################
class VenueNameModal(FroggeModal):

    def __init__(self, cur_val: Optional[str]):

        super().__init__(title="Enter Venue Name")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Venue Name",
                placeholder="eg. 'The Lilypad Lounge'",
                value=cur_val,
                max_length=50,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[0].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################
