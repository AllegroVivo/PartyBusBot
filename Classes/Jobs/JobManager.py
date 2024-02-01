from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import Interaction

from UI import ConfirmCancelView
from Utils import Utilities as U
from .Job import Job

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
    async def load_all(self, data: Dict[str, Any]):
        
        jobs_data = data.get("jobs", [])
        for job_data in jobs_data:
            job = await Job.load(self, job_data)
            self._jobs.append(job)

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
        
        proceed = await self.initial_prompt(interaction)
        if proceed is None or not proceed:
            return
        
        job = Job.new(self, interaction.user)
        self._jobs.append(job)
        
        await job.set_job_details(interaction)
        await job.set_job_schedule(interaction)
        await job.set_job_compensation(interaction)

################################################################################
    @staticmethod
    async def initial_prompt(interaction: Interaction) -> Optional[bool]:

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

                "**When you are ready to begin, click the __Confirm__ button below.**"
            ),
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        return view.value

################################################################################
