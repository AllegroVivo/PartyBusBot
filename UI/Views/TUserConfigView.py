from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle, NotFound
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import TUser, UserConfiguration
################################################################################

__all__ = ("TUserAdminStatusView", "TUserConfigView")

################################################################################
class TUserConfigView(FroggeView):
    
    def __init__(self, user: User, config: UserConfiguration) -> None:
        
        super().__init__(user)
        
        self.config: UserConfiguration = config
        
        button_list = [
            JobPingsButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class JobPingsButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Toggle Job Pings",
            emoji="🔔",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        self.view.config.toggle_job_pings()
        
        status = self.view.config.status()
        await edit_message_helper(interaction, embed=status)
        
        await interaction.edit()
    
################################################################################
