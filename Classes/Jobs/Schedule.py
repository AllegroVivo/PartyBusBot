from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("Schedule",)

################################################################################
class Schedule:

    __slots__ = (
        "_parent",
        "_date",
        "_start",
        "_end",
    )

################################################################################
    def __init__(self, parent: Job, _date: date, start: time, end: time) -> None:
            
        self._parent: Job = parent

        self._date: date = _date
        self._start: time = start
        self._end: time = end
        
################################################################################
    @property
    def date(self) -> date:
        
        return self._date
    
    @date.setter
    def date(self, value: date) -> None:
        
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