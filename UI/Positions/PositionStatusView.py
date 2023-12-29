from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import Position
################################################################################

__all__ = ("PositionStatusView",)

################################################################################
class PositionStatusView(FroggeView):

    def __init__(self, user: User, position: Position):
        
        super().__init__(user)
        
        self.position = position
        
        button_list = [
            PositionNameButton(), PositionRoleButton("Trainer"), PositionRoleButton("Trainee"),
            PositionAddReqButton(), PositionRemoveReqButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class PositionNameButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.edit_name(interaction)
        await interaction.edit(embed=self.view.position.status(), view=self.view)
    
################################################################################
class PositionRoleButton(Button):
    
    def __init__(self, operation: str):
        
        super().__init__(
            style=ButtonStyle.primary,
            label=f"Edit {operation} Role",
            disabled=False,
            row=0
        )
        
        self.operation = operation
        
    async def callback(self, interaction: Interaction):
        await self.view.position.edit_role(interaction, self.operation)
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
################################################################################
class PositionAddReqButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Add Requirement",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.add_requirement(interaction)
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
################################################################################
class PositionRemoveReqButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Remove Requirement",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.remove_requirement(interaction)
        await edit_message_helper(
            interaction, embed=self.view.position.status(), view=self.view
        )
        
################################################################################
