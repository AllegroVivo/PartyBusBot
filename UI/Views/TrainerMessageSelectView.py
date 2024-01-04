from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption
from discord.ui import Select, View

if TYPE_CHECKING:
    from Classes import SignUpMessage
################################################################################

__all__ = ("TrainerMessageSelectView",)

################################################################################
class TrainerMessageSelectView(View):

    def __init__(self, msg: SignUpMessage, options: List[SelectOption]):
        
        super().__init__(timeout=None)
        
        self.message: SignUpMessage = msg
        
        self.complete: bool = False
        self.value = None

        if len(options) == 0:
            options.append(SelectOption(label="None", value="-1"))
            self.add_item(TraineeSelect(options))
        else:
            # Calculate number of TraineeSelect instances needed
            num_trainee_selects = (len(options) // 25) + (1 if len(options) % 25 else 0)
            for i in range(num_trainee_selects):
                # Partition list into chunks of 25
                start, end = i * 25, (i + 1) * 25
                partition = options[start:end]
    
                self.add_item(TraineeSelect(partition))        
            
################################################################################
class TraineeSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a trainee to pick up...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = int(self.values[0])
        self.view.complete = True

        await interaction.edit()
        self.view.stop()
    
################################################################################
