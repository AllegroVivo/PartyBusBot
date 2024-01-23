from __future__ import annotations

from discord import Interaction
from typing import TYPE_CHECKING, List

from .Job import Job

from UI import ConfirmCancelView
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import PartyBusBot
################################################################################

__all__ = ("JobManager",)

################################################################################
class JobManager:

    __slots__ = (
        "_state",
        "_jobs",
    )
    
################################################################################
    def __init__(self, bot: PartyBusBot) -> None:
        
        self._state: PartyBusBot = bot
        
        self._jobs: List[Job] = []
        
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._state
    
################################################################################
    @property
    def jobs(self) -> List[Job]:
        
        return self._jobs

################################################################################
    async def create_post(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Create a New Job Post",
            description=(
                "You must complete **all** of the following prompts to create "
                "a new job post.\n\n"
                
                "__Required Parameters__\n"
                "*(You might want to have these handy during the process!)*\n\n"
                
                "* `Job Type`\n"
                "* `Venue Name`\n"
                "* `Job Description`\n"
                "* `Job Compensation`\n"
                "* `Job Date & Hours`\n"                
                f"{U.draw_line(extra=37)}\n\n"
                
                "**When you are ready to begin, click the **Confirm** button below.**"
            ),
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        await interaction.respond("Done!")

################################################################################
