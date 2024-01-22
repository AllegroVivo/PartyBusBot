from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton, ConfirmCancelView
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import TrainingManager, Training
################################################################################

__all__ = ("AddTrainerSelectView",)

################################################################################
class AddTrainerSelectView(FroggeView):

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
            placeholder="Select a trainee to apply a trainer to...",
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
        self.view.value = trainee
        
        self.view.add_item(TrainingSelect(options))
        
        await interaction.edit(view=self.view)
        
################################################################################
class TrainingSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a training to apply a trainer to...",
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
        self.view.value = (self.view.value, training)

        self.view.add_item(TrainerSelect(options, training))
        
        await interaction.edit(view=self.view)
    
################################################################################
class TrainerSelect(Select):

    def __init__(self, options: List[SelectOption], training: Training):

        if not options:
            options.append(SelectOption(label="None", value="-1"))

        super().__init__(
            placeholder="Select a trainer to apply to the chosen training...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=2
        )
        
        self.training = training
        
    async def callback(self, interaction: Interaction):
        trainer = self.view.mgr.get_trainer(int(self.values[0]))
        
        if self.training.trainer is not None:
            warning = U.make_embed(
                title="Warning!",
                description=(
                    "This training already has a trainer assigned to it. "
                    "Assigning a new trainer will replace the old one. "
                    "Are you sure you want to continue?"
                )
            )
            view = ConfirmCancelView(interaction.user)
            
            await interaction.respond(embed=warning, view=view)
            await view.wait()
            
            if not view.complete or view.value is False:
                return
            
        self.training.trainer = trainer
        self.view.complete = True
        
        await self.view.stop()  # type: ignore
    
################################################################################
