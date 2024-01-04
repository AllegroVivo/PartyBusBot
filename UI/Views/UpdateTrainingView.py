from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import RequirementLevel

if TYPE_CHECKING:
    from Classes import Trainee, Training
################################################################################

__all__ = ("UpdateTrainingView",)

################################################################################
class UpdateTrainingView(FroggeView):

    def __init__(self,  user: User, trainee: Trainee):
        
        super().__init__(user, close_on_complete=True)
        
        self.trainee = trainee
        
        self.add_item(JobPositionSelect([t.position.select_option for t in self.trainee.trainings]))
        self.add_item(CloseMessageButton())
        
################################################################################
class JobPositionSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
                                   
        super().__init__(
            placeholder="Select the position you want to update requirements for...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        training: Training = self.view.trainee.get_training(self.values[0])
        self.view.value = [self.values[0]]
        
        self.placeholder = training.position.name
        self.disabled = True
        
        self.view.add_item(RequirementSelect(training.position.requirement_select_options()))
        await interaction.edit(view=self.view)
    
################################################################################
class RequirementSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        super().__init__(
            placeholder="Select job training requirement to edit...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value.append(self.values[0])
        
        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True

        self.view.add_item(CompletionLevelSelect())
        await interaction.edit(view=self.view)
    
################################################################################
class CompletionLevelSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select the level of completion for that requirement...",
            options=RequirementLevel.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction):
        self.view.value.append(int(self.values[0]))
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
