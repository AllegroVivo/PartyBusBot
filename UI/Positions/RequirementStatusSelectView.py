from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utils import RequirementLevel

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("RequirementStatusSelectView",)

################################################################################
class RequirementStatusSelectView(FroggeView):

    def __init__(self, user: User, options: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(RequirementSelect(options))
        self.add_item(CloseMessageButton())

################################################################################
class RequirementSelect(Select):

    def __init__(self, options: List[SelectOption]):

        if not options:
            options.append(SelectOption(label="None", value="-1"))

        super().__init__(
            placeholder="Select a requirement to update...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.options = options

    async def callback(self, interaction: Interaction):
        self.placeholder = [option.label for option in self.options if option.value == self.values[0]][0]
        self.disabled = True
        
        self.view.add_item(StatusSelect(self.values[0]))
        await interaction.edit(view=self.view)

################################################################################
class StatusSelect(Select):
    
    def __init__(self, req: str):
        
        super().__init__(
            placeholder="Select a status...",
            options=RequirementLevel.select_options(),
            min_values=1,
            max_values=1,
            row=1
        )
        
        self.req = req
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.req, self.values[0]
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
