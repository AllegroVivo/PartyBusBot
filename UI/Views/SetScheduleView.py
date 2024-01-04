from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import TrainingLevel, Weekday, Hours

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("SetScheduleView",)

################################################################################
class SetScheduleView(FroggeView):

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
        self.view.value = [int(self.values[0])]
        
        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True
        
        self.view.add_item(HourSelectA())
        await interaction.edit(view=self.view)
    
################################################################################
class HourSelectA(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select the beginning of your availability...",
            options=Hours.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        value = int(self.values[0])
        self.view.value.append(value)
        
        if value == 0:
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

    def __init__(self, value: int):

        super().__init__(
            placeholder="Select the end of your availability window...",
            options=Hours.adjusted_select_options(value),
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
