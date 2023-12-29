from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Tuple

from Utils import Hours, Timezone, Weekday

if TYPE_CHECKING:
    from Classes import Availability
################################################################################

__all__ = ("TimeRange", )

TR = TypeVar("TR", bound="TimeRange")

################################################################################
class TimeRange:

    __slots__ = (
        "_parent",
        "_start",
        "_end",
    )
    
################################################################################
    def __init__(self, parent: Availability, start: Hours, end: Hours):
        
        self._parent: Availability = parent
        
        self._start: Hours = start
        self._end: Hours = end
        
################################################################################
    @classmethod
    def load(cls: Type[TR], parent: Availability, data: Tuple[int, int, int, int]) -> TR:
        
        return cls(parent, Hours(data[1]), Hours(data[2]))
    
################################################################################
    @property
    def trainee_id(self) -> int:
        
        return self._parent.id
    
################################################################################
    @property
    def day(self) -> Weekday:
        
        return self._day
    
################################################################################
    @property
    def start(self) -> Hours:
        
        return self._start
    
################################################################################
    @property
    def end(self) -> Hours:
        
        return self._end
    
################################################################################
    @property
    def timezone(self) -> Timezone:
        
        return self._timezone
    
################################################################################
