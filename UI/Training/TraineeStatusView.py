from __future__ import annotations

from discord import Interaction, User, Embed, EmbedField, ButtonStyle
from discord.ui import Button
from typing import TYPE_CHECKING, Optional, List

from UI.Common import FroggeView
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import Trainee
################################################################################

__all__ = ("TraineeStatusView", )

################################################################################
class TraineeStatusView(FroggeView):
    
    def __init__(self, user: User, trainee: Trainee) -> None:
        
        super().__init__(user)
        
        self.trainee: Trainee = trainee
        
        button_list = [
            TraineeNameButton(),
            TraineeNotesButton(),
            TraineeAddJobButton(),
            TraineeRemoveJobButton(),
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
class TraineeAddJobButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Request Training(s)",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.trainee.add_jobs(interaction)
        await edit_message_helper(interaction, embed=self.view.trainee.status())

################################################################################
class TraineeRemoveJobButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Remove Training(s)",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.trainee.remove_jobs(interaction)
        await edit_message_helper(interaction, embed=self.view.trainee.status())

################################################################################
