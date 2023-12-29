from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import edit_message_helper, Weekday, Hours, Timezone

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("ScheduleSelectView",)

################################################################################
class ScheduleSelectView(FroggeView):

    def __init__(self, user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.value = {
            "days": [],
            "start": None,
            "end": None,
            "timezone": None
        }
        
        button_list = [
            WeekdaySelect(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class WeekdaySelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a weekday(s) to add availability for...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=len(Weekday.select_options()),
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value["days"] = [Weekday(int(v)) for v in self.values]
        
        if len(self.values) == 1:
            self.placeholder = self.view.value["days"][0].proper_name
        self.disabled = True
        
        self.view.add_item(TimeSelect("start"))        
        await interaction.edit(view=self.view)
        
################################################################################
class TimeSelect(Select):
    
    def __init__(self, operation: str):
        
        super().__init__(
            placeholder=f"{operation.capitalize()} of Availability...",
            options=Hours.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1 if operation == "start" else 2
        )
        
        self.operation = operation
        
    async def callback(self, interaction: Interaction):
        time = Hours(int(self.values[0]))
        self.view.value[self.operation] = time
        
        self.placeholder = f"{self.operation.capitalize()}: {time.proper_name}"
        self.disabled = True

        new_item = TimeSelect("end") if self.operation == "start" else TimezoneSelect()
        self.view.add_item(new_item)
        
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
            row=3
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value["timezone"] = Timezone(int(self.values[0]))
        
        await interaction.edit(view=self.view)
        await self.view.stop()  # type: ignore
        
################################################################################
