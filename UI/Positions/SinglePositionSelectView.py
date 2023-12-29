from __future__ import annotations

from discord import Interaction, SelectOption, User
from discord.ui import Select
from typing import TYPE_CHECKING, Optional, List

from Utils import TrainingLevel
from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("SinglePositionSelectView",)

################################################################################
class SinglePositionSelectView(FroggeView):

    def __init__(self, user: User, positions: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(PositionSelect(positions))
        self.add_item(CloseMessageButton())
        
################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a position to request training for...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True
        
        await interaction.edit(view=self.view)
        await self.view.stop()  # type: ignore
    
################################################################################
