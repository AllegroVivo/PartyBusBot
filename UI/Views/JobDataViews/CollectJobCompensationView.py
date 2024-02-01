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

__all__ = ("CollectJobCompensationView",)

################################################################################
class CollectJobCompensationView(_CollectJobDataView):
    
    def __init__(self, user: User, job: Job) -> None:
        
        super().__init__(user, job)
        
        button_list = [
            _PositionButton(),
            _VenueButton(),
            _DescriptionButton(),
            ContinueButton(),
            CancelButton()
        ]
        
        for button in button_list:
            self.add_item(button)
            
        self.set_component_properties()

################################################################################        
    def set_component_properties(self) -> None:

        self.children[0].style = (  # type: ignore
            ButtonStyle.secondary if self.job.position is None else ButtonStyle.primary
        )
        self.children[1].style = (  # type: ignore
            ButtonStyle.secondary if self.job.venue is None else ButtonStyle.primary
        )
        self.children[2].style = (  # type: ignore
            ButtonStyle.secondary if self.job.description is None else ButtonStyle.primary
        )
        self.children[3].disabled = (  # type: ignore
            True if self.job.position is None or self.job.venue is None 
            else False
        )
    
################################################################################
class _PositionButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Select Job",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.details.set_position(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.details_status,
            view=self.view
        )
        
################################################################################
class _VenueButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set Venue",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.details.set_venue(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.details_status,
            view=self.view
        )
        
################################################################################
class _DescriptionButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set Description",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.job.details.set_description(interaction)
        self.view.set_component_properties()
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.job.details_status,
            view=self.view
        )
        
################################################################################
