from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import TrainingManager
################################################################################

__all__ = ("RemoveTrainerSelectView",)

################################################################################
class RemoveTrainerSelectView(FroggeView):

    def __init__(self, user: User, training_mgr: TrainingManager):
        
        super().__init__(user, close_on_complete=True)
        
        self.mgr: TrainingManager = training_mgr
        
        def split_list(input_list):
            return [input_list[i:i + 24] for i in range(0, len(input_list), 24)]
        
        options = self.mgr.trainee_options()
        options = split_list(options)
        
        for option_list in options:
            self.add_item(TraineeSelect(option_list))
        self.add_item(CloseMessageButton())
        
    
################################################################################
class TraineeSelect(Select):

    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
        
        super().__init__(
            placeholder="Select a trainee to remove a trainer from...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        trainee = self.view.mgr.get_trainee(int(self.values[0]))
        trainings = trainee.trainings
        options = [t.select_option for t in trainings]
        
        self.placeholder = trainee.name
        self.disabled = True
        
        self.view.add_item(TrainingSelect(options))
        
        await interaction.edit(view=self.view)
        
################################################################################
class TrainingSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a training to remove the trainer from...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        training = self.view.mgr.get_training_by_id(self.values[0])
        trainers = self.view.mgr.get_qualified_trainers(training.position.id)
        options = [t.select_option for t in trainers]
        
        self.placeholder = training.position.name
        self.disabled = True
        self.view.value = training

        self.view.add_item(TrainerSelect(options))
        
        await interaction.edit(view=self.view)
    
################################################################################
class TrainerSelect(Select):

    def __init__(self, options: List[SelectOption]):

        if not options:
            options.append(SelectOption(label="None", value="-1"))

        super().__init__(
            placeholder="Pick a trainer to remove from the chosen training...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=2
        )
        
    async def callback(self, interaction: Interaction):
        trainer = self.view.mgr.get_trainer(int(self.values[0]))
        self.view.value.trainer = None
        
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
