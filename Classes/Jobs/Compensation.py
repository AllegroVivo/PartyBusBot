from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from Utils import CompensationType

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("Compensation",)

################################################################################
class Compensation:

    __slots__ = (
        "_parent",
        "_rate",
        "_type",
    )
    
################################################################################
    def __init__(
        self, 
        parent: Job,
        rate: Optional[int] = None,
        _type: Optional[CompensationType] = None
    ) -> None:
        
        self._parent: Job = parent
        
        self._rate: int = rate
        self._type: CompensationType = _type
        
################################################################################
    @property
    def pay_rate(self) -> int:
        
        return self._rate
    
    @pay_rate.setter
    def pay_rate(self, value: int) -> None:
        
        self._rate = value
        self.update()
        
################################################################################
    @property
    def pay_type(self) -> CompensationType:
        
        return self._type
    
    @pay_type.setter
    def pay_type(self, value: CompensationType) -> None:
        
        self._type = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
