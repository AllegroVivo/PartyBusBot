from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import Trainee, TrainingManager
################################################################################

__all__ = ("TrainerAssignmentStatusView",)

################################################################################
class TrainerAssignmentStatusView(FroggeView):
    
    def __init__(self, user: User, training_manager: TrainingManager):
        
        super().__init__(user)
        
        self.mgr: TrainingManager = training_manager

        button_list = [
            AddTrainerButton(),
            RemoveTrainerButton(),
            CloseMessageButton()
        ]
        
        for btn in button_list:
            self.add_item(btn)
            
        self.set_buttons()
            
################################################################################
    def set_buttons(self) -> None:

        disable_add = False if len(self.mgr.all_trainings) > 0 else True
        disable_remove = False
        if len(self.mgr.all_trainings) == 0:
            disable_remove = True
        if not any(t.trainer is not None for t in self.mgr.all_trainings):
            disable_remove = True
            
        self.children[0].disabled = disable_add  # type: ignore
        self.children[1].disabled = disable_remove  # type: ignore
    
################################################################################
class AddTrainerButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Trainer to Trainee",
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.mgr.add_trainer_to_training(interaction)
        
        self.view.set_buttons()

        await edit_message_helper(
            interaction,
            embed=self.view.mgr.manage_trainers_embed(),
            view=self.view
        )
        
################################################################################
class RemoveTrainerButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Trainer from Trainee",
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.mgr.remove_trainer_from_training(interaction)

        self.view.set_buttons()

        await edit_message_helper(
            interaction,
            embed=self.view.mgr.manage_trainers_embed(),
            view=self.view
        )
        
################################################################################
