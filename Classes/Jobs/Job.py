from __future__ import annotations

from datetime import date, time
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Type, TypeVar, Optional

from .Compensation import Compensation
from .Details import JobDetails
from .Schedule import Schedule
from .Users import JobUsers

from Utils import CompensationType

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
    def new(
        cls: Type[J], 
        manager: JobManager,
        position: Position,
        venue: str,
        description: Optional[str],
        _date: date,
        start: time,
        end: time,
        pay: int,
        pay_type: CompensationType,
        requester: User,
        applicant: User
    ) -> J:
        
        self: J = cls.__new__(cls)
        
        self._id = manager.bot.database.new.job(
            position,
            venue,
            description,
            _date,
            start,
            end,
            pay,
            pay_type,
            requester,
            applicant
        )
        self._manager = manager
        
        self._users = JobUsers(self, requester, applicant)
        self._details = JobDetails(self, position, venue, description)
        self._schedule = Schedule(self, _date, start, end)
        self._compensation = Compensation(self, pay, pay_type)
        
        return self
        
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._manager.bot
    
################################################################################
    @property
    def position(self) -> Position:
        
        return self._details.position
    
################################################################################
    @property
    def venue(self) -> str:
        
        return self._details.venue
    
################################################################################
    @property
    def description(self) -> str:
        
        return self._details.description
    
################################################################################
    @property
    def job_date(self) -> date:
        
        return self._schedule.date
    
################################################################################
    @property
    def start_time(self) -> time:
        
        return self._schedule.start_time
    
################################################################################
    @property
    def end_time(self) -> time:
        
        return self._schedule.end_time
    
################################################################################
    @property
    def pay_rate(self) -> int:
        
        return self._compensation.pay_rate
    
################################################################################
    @property
    def pay_type(self) -> CompensationType:
        
        return self._compensation.pay_type
    
################################################################################    
    @property
    def requester(self) -> User:
        
        return self._users.requester
    
################################################################################
    @property
    def applicant(self) -> User:
        
        return self._users.applicant
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.job(self)
        
################################################################################
