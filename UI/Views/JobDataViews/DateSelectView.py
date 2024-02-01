from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, User, SelectOption
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import Month, edit_message_helper, Days

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("DateSelectView",)

################################################################################
class DateSelectView(FroggeView):

    def __init__(self, user: User, job: Job):
        
        super().__init__(user, close_on_complete=True)
        
        self.job: Job = job
        
        self.month: Month = None  # type: ignore
        self.day: Days = None  # type: ignore
        
        self.add_item(MonthSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class MonthSelect(Select):

    def __init__(self):
        
        super().__init__(
            placeholder="Select the month of the job opening...",
            options=Month.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.month = Month(int(self.values[0]))
        self.placeholder = self.view.month.proper_name
        
        self.view.add_item(DaySelect(self.view.month.day_options()[:15], 1))
        self.view.add_item(DaySelect(self.view.month.day_options()[15:], 2))
        
        await interaction.edit(embed=self.view.job.schedule_status, view=self.view)
        
################################################################################
class DaySelect(Select):

    def __init__(self, options: List[SelectOption], row: int):
        
        super().__init__(
            placeholder="Select the day of the open shift...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=False,
            row=row
        )
        
    async def callback(self, interaction: Interaction):
        self.view.day = Days(int(self.values[0]))
        
        self.view.value = (self.view.month, self.view.day)
        self.view.complete = True

        await interaction.edit(embed=self.view.job.schedule_status, view=self.view)
        await self.view.stop()  # type: ignore
        
################################################################################
