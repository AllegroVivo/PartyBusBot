from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("JobDescriptionModal",)

################################################################################
class JobDescriptionModal(FroggeModal):

    def __init__(self, cur_val: Optional[str]):

        super().__init__(title="Enter Job Description")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Include any additional information below.",
                value=(
                    "Enter any additional information you would like to "
                    "pass along to potential temporary employees in the "
                    "box below. (Leave blank to clear it!)"
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Description Text",
                placeholder="eg. 'Pants Optional'",
                value=cur_val,
                max_length=250,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value or "-"
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################
