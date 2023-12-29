from __future__ import annotations

from discord import Interaction, InputTextStyle
from discord.ui import InputText
from typing import TYPE_CHECKING, Optional

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("NameModal",)

################################################################################
class NameModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Name")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a new name.",
                value="Enter a new name or edit the currently existing one.",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Name",
                placeholder="eg. 'Allegro Vivo'",
                value=cur_val,
                max_length=30,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################
