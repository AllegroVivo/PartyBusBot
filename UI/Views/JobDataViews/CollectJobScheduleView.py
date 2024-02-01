from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import CancelButton, ContinueButton
from Utils import edit_message_helper
from .CollectJobDataView import _CollectJobDataView

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("CollectJobScheduleView",)

################################################################################
class CollectJobScheduleView(_CollectJobDataView):
    
    def __init__(self, user: User, job: Job) -> None:
        
        super().__init__(user, job)
        
        button_list = [
            _DateButton(),
            _StartTimeButton(),
            _EndTimeButton(),
            ContinueButton(),
            CancelButton()
        ]
        
        for button in button_list:
            self.add_item(button)
            
        self.set_component_properties()
            
################################################################################        
    def set_component_properties(self) -> None:

        self.children[0].style = (  # type: ignore
            ButtonStyle.secondary if self.job.job_date is None else ButtonStyle.primary
        )
        self.children[1].style = (  # type: ignore
            ButtonStyle.secondary if self.job.start_time is None else ButtonStyle.primary
        )
        self.children[2].style = (  # type: ignore
            ButtonStyle.secondary if self.job.end_time is None else ButtonStyle.primary
        )
        self.children[3].disabled = (  # type: ignore
            True if self.job.job_date is None or self.job.start_time is None 
            or self.job.end_time is None else False
        )
        
################################################################################
class _DateButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Edit Date",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.schedule.set_date(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.schedule_status,
            view=self.view
        )
        
################################################################################
class _StartTimeButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set Start Time",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.schedule.set_start_time(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.schedule_status,
            view=self.view
        )
        
################################################################################
class _EndTimeButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set End Time",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.schedule.set_end_time(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.schedule_status,
            view=self.view
        )
        
################################################################################
