from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Classes import Position
################################################################################

__all__ = ("JobDetails",)

################################################################################
class JobDetails:

    __slots__ = (
        "_parent",
        "_position",
        "_venue",
        "_description",
    )

    ################################################################################
    def __init__(
        self, 
        parent: JobDetails, 
        position: Position, 
        venue: str, 
        description: Optional[str] = None
    ) -> None:

        self._parent: JobDetails = parent

        self._position: Position = position
        self._venue: str = venue
        self._description: Optional[str] = description

################################################################################
    @property
    def position(self) -> Position:
        
        return self._position
    
    @position.setter
    def position(self, value: Position) -> None:
        
        self._position = value
        self.update()
        
################################################################################
    @property
    def venue(self) -> str:
        
        return self._venue
    
    @venue.setter
    def venue(self, value: str) -> None:
        
        self._venue = value
        self.update()
        
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]) -> None:
        
        self._description = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
