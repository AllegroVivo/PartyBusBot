from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List

from discord import Interaction, User, SelectOption
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import Hours, Minutes, Timezone, ViewType

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("TimeSelectView",)

################################################################################
class TimeSelectView(FroggeView):

    def __init__(self,  user: User, viewtype: ViewType):
        
        super().__init__(user, close_on_complete=True)
        
        options = (
            Hours.select_options() if viewtype == ViewType.StartTimeSelect 
            else Hours.limited_select_options()
        )
        
        self.add_item(HourSelectA(options))
        self.add_item(CloseMessageButton())
    
################################################################################
class HourSelectA(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        super().__init__(
            placeholder="Select the beginning of your availability...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        value = int(self.values[0])
        self.view.value = value
        
        if value == 0:  # Unavailable
            self.view.value = -1
            self.view.complete = True
            await interaction.edit()
            await self.view.stop()  # type: ignore
            return

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True

        self.view.add_item(HourSelectB(value))
        await interaction.edit(view=self.view)
    
################################################################################
class HourSelectB(Select):

    def __init__(self, hour: int):

        super().__init__(
            placeholder="Select the minutes...",
            options=Minutes.hour_specific_select_options(hour),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        self.view.value = time(self.view.value - 1, int(self.values[0]))  # type: ignore

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True
        
        self.view.add_item(TimezoneSelect())
        await interaction.edit(view=self.view)

################################################################################
class TimezoneSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select your timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction):
        adj_hour = self.view.value.hour - Timezone(int(self.values[0])).utc_offset
        if adj_hour < 0:
            adj_hour += 24
        elif adj_hour > 23:
            adj_hour -= 24        
        
        self.view.value = time(adj_hour, self.view.value.minute) 
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
