from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import Trainee
################################################################################

__all__ = ("TrainerAssignmentStatusView",)

################################################################################
class TrainerAssignmentStatusView(FroggeView):
    
    def __init__(self,  user: User, trainee: Trainee):
        
        super().__init__(user)
        
        self.trainee: Trainee = trainee
        
        button_list = [
            AddTrainerButton(),
            CloseMessageButton()
        ]
        
        for btn in button_list:
            self.add_item(btn)
            
################################################################################
class AddTrainerButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Trainer to Trainee",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.trainee.add_trainer(interaction.user)
        
################################################################################
