from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple

from Utils import Weekday, Hours

if TYPE_CHECKING:
    from Classes import PartyBusBot, TUser
################################################################################

__all_ = ("Availability",)

A = TypeVar("A", bound="Availability")

################################################################################
class Availability:

    __slots__ = (
        "_parent",
        "_day",
        "_start",
        "_end",
    )
    
################################################################################
    def __init__(self, parent: TUser, day: Weekday, start: Hours, end: Hours) -> None:
        
        self._parent: TUser = parent
        
        self._day: Weekday = day
        self._start: Hours = start
        self._end: Hours = end        
        
################################################################################
    @classmethod
    def new(cls, parent: TUser, data: Tuple[Any, ...]) -> A:
        
        parent.bot.database.insert.availability(parent.user_id, *data)
        return cls(
            parent,
            Weekday(data[0]),
            Hours(data[1]),
            Hours(data[2]) if data[2] is not None else None
        )
    
################################################################################
    @classmethod
    def load(cls: Type[A], parent: TUser, data: Tuple[Any, ...]) -> A:
        
        return cls(
            parent,
            Weekday(data[1]),
            Hours(data[2]),
            Hours(data[3]) if data[3] is not None else None
        )
    
################################################################################
    @property
    def day(self) -> Weekday:
        
        return self._day
    
################################################################################
    @property
    def start_time(self) -> Hours:
        
        return self._start
    
################################################################################
    @property
    def end_time(self) -> Hours:
        
        return self._end
    
################################################################################
    @property
    def start_timestamp(self) -> str:
        
        return self._start.timestamp
    
################################################################################
    @property
    def end_timestamp(self) -> str:
        
        return self._end.timestamp
    
################################################################################
    @staticmethod
    def availability_status(availability: List[Availability]) -> str:
        
        if not availability:
            return "`No Availability Set`"   
        
        ret = ""
        
        for i in [w for w in Weekday if w.value != 0]:
            if i.value not in [a.day.value for a in availability]:
                ret += f"{i.proper_name}: `Not Available`\n"
            else:
                a = [a for a in availability if a.day == i][0]
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )
        
        return ret
    
################################################################################
    