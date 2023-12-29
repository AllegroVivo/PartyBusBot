from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple

from Utils import Weekday, Hours

if TYPE_CHECKING:
    pass
################################################################################

__all_ = ("Availability",)

A = TypeVar("A", bound="Availability")

################################################################################
class Availability:

    __slots__ = (
        "_day",
        "_start",
        "_end",
    )
    
################################################################################
    def __init__(self, day: Weekday, start: Hours, end: Hours) -> None:
        
        self._day: Weekday = day
        self._start: Hours = start
        self._end: Hours = end        
        
################################################################################
    @classmethod
    def load(cls: Type[A], data: Tuple[Any, ...]) -> A:
        
        return cls(
            Weekday(data[1]),
            Hours(data[2]),
            Hours(data[3])
        )
    
################################################################################
