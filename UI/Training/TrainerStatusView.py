from __future__ import annotations

from discord import Interaction, ButtonStyle, User
from discord.ui import Button
from typing import TYPE_CHECKING, Optional, List

from UI.Common import FroggeView
from Utils import edit_message_helper, JobPosition

if TYPE_CHECKING:
    from Classes import Trainer
################################################################################

__all__ = ("TrainerStatusView", )

################################################################################
class TrainerStatusView(FroggeView):

    def __init__(self, user: User, trainer: Trainer):
        
        super().__init__(user)
        
        self.trainer: Trainer = trainer
        
        button_list = [
            TrainerNameButton(trainer.name),
            AddTrainerPositionsButton(),
            TrainerNotesButton()
        ]
        
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class TrainerNameButton(Button):
    
    def __init__(self, name: Optional[str]):
        
        super().__init__(
            style=ButtonStyle.secondary if name is None else ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.trainer.edit_name(interaction)
        
        self.style = ButtonStyle.primary
        
        await interaction.edit(embed=self.view.trainer.status(), view=self.view)
    
################################################################################
class AddTrainerPositionsButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Qualification(s)",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.trainer.edit_qualifications(interaction)
        await edit_message_helper(interaction, embed=self.view.trainer.status())
    
################################################################################
class TrainerNotesButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Notes",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.trainer.edit_notes(interaction)
        await interaction.edit(embed=self.view.trainer.status())
        
################################################################################
