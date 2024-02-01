from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, SelectOption
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import Month, Hours, edit_message_helper, Minutes, Timezone

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("TimeSelectView",)

################################################################################
class TimeSelectView(FroggeView):

    def __init__(self, user: User, job: Job):
        
        super().__init__(user, close_on_complete=True)
        
        self.job: Job = job
        
        self.hour: int = None  # type: ignore
        self.minute: int = None  # type: ignore
        self.tz: Timezone = None  # type: ignore
        
        self.add_item(HourSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class HourSelect(Select):

    def __init__(self):
        
        super().__init__(
            placeholder="Select the hour of the job's start time...",
            options=Hours.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.hour = int(self.values[0]) + 1
        self.view.add_item(MinuteSelect(self.view.hour))
        
        for option in self.options:
            if option.value == self.values[0]:
                self.placeholder = option.label
        
        await interaction.edit(view=self.view)
        
################################################################################
class MinuteSelect(Select):

    def __init__(self, hour: int):
        
        if hour == 0:
            hour = 12
        if hour > 12:
            hour -= 12
        
        options = Minutes.select_options()
        for o in options:
            o.label = f"{hour}{o.label}"
        
        super().__init__(
            placeholder="Select the minute of the job's start time...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.minute = (int(self.values[0]) - 1) * 15
        self.view.add_item(TimezoneSelect())

        for option in self.options:
            if option.value == self.values[0]:
                self.placeholder = option.label

        await interaction.edit(view=self.view)
        
################################################################################
class TimezoneSelect(Select):

    def __init__(self):
        
        super().__init__(
            placeholder="Select the timezone of the job's start time...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )
        
    async def callback(self, interaction: Interaction):
        self.view.tz = Timezone(int(self.values[0]))
        self.view.value = (
            self.view.hour, 
            self.view.minute, 
            self.view.tz
        )
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore
        
################################################################################
