from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction, Embed
from UI import DateSelectView, CollectJobScheduleView, TimeSelectView
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("Schedule",)

S = TypeVar("S", bound="Schedule")

################################################################################
class Schedule:

    __slots__ = (
        "_parent",
        "_date",
        "_start",
        "_end",
    )

################################################################################
    def __init__(
        self, 
        parent: Job, 
        _date: Optional[date] = None,
        start: Optional[time] = None, 
        end: Optional[time] = None
    ) -> None:
            
        self._parent: Job = parent

        self._date: Optional[date] = _date
        self._start: Optional[time] = start
        self._end: Optional[time] = end
        
################################################################################
    @classmethod
    def load(cls: Type[S], parent: Job, data: Tuple[Any, ...]) -> Schedule:
        
        return cls(parent, data[0], data[1], data[2])
    
################################################################################
    @property
    def job_date(self) -> date:
        
        return self._date
    
    @job_date.setter
    def job_date(self, value: job_date) -> None:
        
        self._date = value
        self.update()
        
################################################################################
    @property
    def start_time(self) -> time:
        
        return self._start
    
    @start_time.setter
    def start_time(self, value: time) -> None:
        
        self._start = value
        self.update()
        
################################################################################
    @property
    def end_time(self) -> time:
        
        return self._end
    
    @end_time.setter
    def end_time(self, value: time) -> None:
        
        self._end = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
    async def set_all(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = CollectJobScheduleView(interaction.user, self._parent)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
    
################################################################################
    def status(self) -> Embed:
        
        date_val = start_val = end_val = "`Not Set`"
        
        if self.job_date is not None:
            date_val = U.format_dt(U.date_to_datetime(self.job_date), "d")
        if self.start_time is not None:
            start_val = U.format_dt(U.time_to_datetime(self.start_time), "t")
        if self.end_time is not None:
            end_val = U.format_dt(U.time_to_datetime(self.end_time), "t")
        
        return U.make_embed(
            title="Job Schedule",
            description=(
                f"**Date:** {date_val}\n"
                f"**Start Time:** {start_val}\n"
                f"**End Time:** {end_val}\n"
                f"{U.draw_line(extra=25)}\n\n"

                "Please complete the above details before continuing."
            ),
        )
    
################################################################################
    async def set_date(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Set Date",
            description=(
                "Please enter the **month** of the job from "
                "the following drop-downs."
            ),
        )
        view = DateSelectView(interaction.user, self._parent)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.job_date = date(
            month=view.value[0].value, 
            day=view.value[1].value, 
            year=date.today().year
        )
        
################################################################################
    async def set_start_time(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Set Start Time",
            description=(
                "Please enter the **start time** of the job from "
                "the following drop-downs."
            ),
        )
        view = TimeSelectView(interaction.user, self._parent)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        hour, minute, tz = view.value
        _time = time(hour, minute, second=0)
        
        self.start_time = U.shift_time(_time, tz)
    
################################################################################
    async def set_end_time(self, interaction: Interaction) -> None:

        embed = U.make_embed(
            title="Set Start Time",
            description=(
                "Please enter the **end time** of the job from "
                "the following drop-downs."
            ),
        )
        view = TimeSelectView(interaction.user, self._parent)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        hour, minute, tz = view.value
        _time = time(hour, minute, second=0)

        self.end_time = U.shift_time(_time, tz)
    
################################################################################
