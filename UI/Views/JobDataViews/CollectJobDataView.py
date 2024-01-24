from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle, NotFound
from discord.ui import Button

from UI.Common import FroggeView, CancelButton
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import TUser, Job
################################################################################

__all__ = ("_CollectJobDataView",)

################################################################################
class _CollectJobDataView(FroggeView):
    
    def __init__(self, user: User, job: Job) -> None:
        
        super().__init__(user)
        self.job: Job = job

################################################################################        
    def set_style(self) -> None:
         
        raise NotImplementedError
    
################################################################################
