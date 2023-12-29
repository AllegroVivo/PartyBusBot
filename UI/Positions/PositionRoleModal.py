from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("PositionRoleModal",)

################################################################################
class PositionRoleModal(FroggeModal):

    def __init__(self):

        super().__init__(title="Edit Role Assignment")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the new linked Role ID for this job...",
                value=(
                    "Enter the new linked Role ID for this job...\n"
                    "This should be between 17 and 19 digits long.\n"
                ),
                required=False
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Role ID",
                placeholder="eg. '123456789012345678'",
                min_length=17,
                max_length=19,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################
