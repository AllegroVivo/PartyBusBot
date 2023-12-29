from __future__ import annotations

from discord import Interaction, User, Embed, EmbedField, ButtonStyle
from discord.ui import Button
from typing import TYPE_CHECKING, Optional, List

from UI.Common import FroggeView
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import Trainee
################################################################################

__all__ = ("UpdateTraineeView",)

################################################################################
class UpdateTraineeView(FroggeView):
    
    def __init__(self, user: User, trainee: Trainee) -> None:
        
        super().__init__(user)
        
        self.trainee: Trainee = trainee
        
        button_list = [
            TraineeNameButton(),
            TraineeRequirementsButton(disabled=True if not self.trainee.trainings else False),
            TraineeNotesButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class TraineeNameButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.trainee.set_name(interaction)
        await interaction.edit(embed=self.view.trainee.status())

################################################################################
class TraineeNotesButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.primary,
            label="Notes",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.trainee.edit_notes(interaction)
        await interaction.edit(embed=self.view.trainee.status())

################################################################################
class TraineeRequirementsButton(Button):
    
    def __init__(self, disabled: bool) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Update Requirements",
            disabled=disabled,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.trainee.update_requirements(interaction)
        await edit_message_helper(interaction, embed=self.view.trainee.status())
        
################################################################################
