from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle, NotFound
from discord.ui import Button

from UI.Common import FroggeView
from Utils import edit_message_helper

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("TUserStatusView",)

################################################################################
class TUserStatusView(FroggeView):
    
    def __init__(self, user: User, tuser: TUser) -> None:
        
        super().__init__(user)
        
        self.tuser: TUser = tuser
        
        button_list = [
            EditNameButton(),
            EditNotesButton(),
            AddQualificationButton(),
            ModifyQualificationButton(),
            RemoveQualificationButton(),
            AddTrainingButton(),
            RemoveTrainingButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_buttons()
        
################################################################################        
    def set_buttons(self) -> None:
        
        disable_buttons = True if len(self.tuser.qualifications) == 0 else False
        
        self.children[3].disabled = disable_buttons
        self.children[4].disabled = disable_buttons
        
################################################################################
class EditNameButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_name(interaction)
        await interaction.edit(embed=self.view.tuser.status())
        
################################################################################
class EditNotesButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Notes",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_notes(interaction)
        await interaction.edit(embed=self.view.tuser.status())
        
################################################################################
class AddQualificationButton(Button):
        
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Qualification",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.add_qualification(interaction)
        
        self.view.set_buttons()
        
        await edit_message_helper(interaction, embed=self.view.tuser.status(), view=self.view)
      
################################################################################
class ModifyQualificationButton(Button):

    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Qualification",
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.modify_qualification(interaction)

        self.view.set_buttons()
        
        await edit_message_helper(interaction, embed=self.view.tuser.status(), view=self.view)
        
################################################################################
class RemoveQualificationButton(Button):
        
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Qualification",
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.remove_qualification(interaction)
        
        self.view.set_buttons()
        
        await edit_message_helper(interaction, embed=self.view.tuser.status(), view=self.view)
        
################################################################################
class AddTrainingButton(Button):
            
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Training",
            row=2
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.add_training(interaction)
        
        self.view.set_buttons()
        
        await edit_message_helper(interaction, embed=self.view.tuser.status(), view=self.view)


################################################################################
class RemoveTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Training",
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.remove_training(interaction)

        self.view.set_buttons()

        await edit_message_helper(interaction, embed=self.view.tuser.status(), view=self.view)
        
################################################################################
