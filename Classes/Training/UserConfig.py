from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Tuple, Any

from Utils import Timezone

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("UserConfiguration",)

UC = TypeVar("UC", bound="UserConfiguration")

################################################################################
class UserConfiguration:

    __slots__ = (
        "_parent",
        "_image",
        "_timezone",
    )
    
################################################################################
    def __init__(self, parent: TUser, image: Optional[str] = None, timezone: Optional[Timezone] = None):
        
        self._parent: TUser = parent
        
        self._image: Optional[str] = image
        self._timezone: Optional[Timezone] = timezone
        
################################################################################
    @classmethod
    def load(cls: Type[UC], parent: TUser, data: Tuple[Any, ...]) -> UC:
        
        return cls(parent, data[1], (Timezone(data[2]) if data[2] is not None else None))
    
################################################################################
