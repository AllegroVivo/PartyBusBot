from __future__ import annotations

from typing import TYPE_CHECKING

from discord import User

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("JobUsers",)

################################################################################
class JobUsers:

    __slots__ = (
        "_parent",
        "_requestor",
        "_applicant",
    )

    ################################################################################
    def __init__(self, parent: Job, requestor: User, applicant: User) -> None:

        self._parent: Job = parent
        
        self._requestor: User = requestor
        self._applicant: User = applicant

################################################################################
    @property
    def requestor(self) -> User:
        
        return self._requestor
    
    @requestor.setter
    def requestor(self, value: User) -> None:
        
        self._requestor = value
        self.update()
        
################################################################################
    @property
    def applicant(self) -> User:
        
        return self._applicant
    
    @applicant.setter
    def applicant(self, value: User) -> None:
        
        self._applicant = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
