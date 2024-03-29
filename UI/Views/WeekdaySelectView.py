from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import TrainingLevel, Weekday, Hours

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("WeekdaySelectView",)

################################################################################
class WeekdaySelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(WeekdaySelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class WeekdaySelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a day of the week to set availability for...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = Weekday(int(self.values[0]))
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
