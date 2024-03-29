from __future__ import annotations

from datetime import date, time
from discord import Interaction, User, Embed, NotFound, HTTPException
from typing import TYPE_CHECKING, List, Type, TypeVar, Optional, Tuple, Dict, Any

from .Compensation import Compensation
from .Details import JobDetails
from .Schedule import Schedule
from .Users import JobUsers

from Utils import Utilities as U, CompensationType

if TYPE_CHECKING:
    from Classes import JobManager, Position, PartyBusBot
################################################################################

__all__ = ("Job",)

J = TypeVar("J", bound="Job")

################################################################################
class Job:

    __slots__ = (
        "_id",
        "_manager",
        "_users",
        "_details",
        "_schedule",
        "_compensation",
    )
    
################################################################################
    def __init__(
        self,
        _id: str,
        manager: JobManager, 
        users: JobUsers,
        details: JobDetails, 
        schedule: Schedule,
        compensation: Compensation
    ) -> None:
        
        self._id: str = _id
        self._manager: JobManager = manager
        
        self._users: JobUsers = users
        self._details: JobDetails = details
        self._schedule: Schedule = schedule
        self._compensation: Compensation = compensation
        
################################################################################
    @classmethod
    def new(cls: Type[J], manager: JobManager, requester: User) -> J:

        self: J = cls.__new__(cls)
        
        self._id = manager.bot.database.insert.job(requester.id)
        self._manager = manager
        
        self._users = JobUsers(self, requester)
        self._details = JobDetails(self)
        self._schedule = Schedule(self)
        self._compensation = Compensation(self)
        
        return self
    
################################################################################    
    @classmethod
    async def load(cls: Type[J], manager: JobManager, data: Tuple[Any, ...]) -> J:

        requestor = manager.bot.get_user(data[9])
        applicant = manager.bot.get_user(data[10])

        if requestor is None:
            try: 
                requestor = await manager.bot.fetch_user(data[9])
            except (NotFound, HTTPException):
                requestor = None
                
        if applicant is None:
            try:
                applicant = await manager.bot.fetch_user(data[10])
            except (NotFound, HTTPException):
                applicant = None
        
        self: J = cls.__new__(cls)
        
        self._id = data[0]
        self._manager = manager
        
        self._users = JobUsers.load(self, requestor, applicant)
        self._details = JobDetails.load(self, data[1:4])
        self._schedule = Schedule.load(self, data[4:7])
        self._compensation = Compensation.load(self, data[7:9])
        
        return self
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._manager.bot
    
################################################################################
    @property
    def details(self) -> JobDetails:
        
        return self._details
    
################################################################################
    @property
    def schedule(self) -> Schedule:
        
        return self._schedule
    
################################################################################
    @property
    def compensation(self) -> Compensation:
        
        return self._compensation
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def position(self) -> Optional[Position]:
        
        return self._details.position
    
################################################################################
    @property
    def venue(self) -> Optional[str]:
        
        return self._details.venue
    
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._details.description
    
################################################################################
    @property
    def job_date(self) -> Optional[date]:
        
        return self._schedule.job_date
    
################################################################################
    @property
    def start_time(self) -> Optional[time]:
        
        return self._schedule.start_time
    
################################################################################
    @property
    def end_time(self) -> Optional[time]:
        
        return self._schedule.end_time
    
################################################################################
    @property
    def pay_rate(self) -> Optional[int]:
        
        return self._compensation.pay_rate
    
################################################################################
    @property
    def pay_type(self) -> Optional[CompensationType]:
        
        return self._compensation.pay_type
    
################################################################################    
    @property
    def requestor(self) -> User:
        
        return self._users.requestor
    
################################################################################
    @property
    def applicant(self) -> Optional[User]:
        
        return self._users.applicant
    
################################################################################
    @property
    def details_status(self) -> Embed:

        return self._details.status()

################################################################################
    @property
    def schedule_status(self) -> Embed:

        return self._schedule.status()
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.job(self)
    
################################################################################
    async def set_job_details(self, interaction: Interaction) -> None:
        
        await self._details.set_all(interaction)
    
################################################################################
    async def set_job_schedule(self, interaction: Interaction) -> None:
        
        await self._schedule.set_all(interaction)
        
################################################################################
    async def set_job_compensation(self, interaction: Interaction) -> None:
        
        await self._compensation.set_all(interaction)
        
################################################################################
