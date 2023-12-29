from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Tuple, Dict

from discord import SelectOption
from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import PartyBusBot
    from Utils import RequirementLevel
################################################################################

__all__ = ("Requirement", )

R = TypeVar("R", bound="Requirement")

################################################################################
class Requirement:
    
    __slots__ = (
        "_state",
        "_id",
        "_parent_id",
        "_description"
    )
    
################################################################################
    def __init__(self, bot: PartyBusBot, _id: str, pos_id: str, description: str) -> None:
        
        self._state: PartyBusBot = bot
        
        self._id: str = _id
        self._parent_id: str = pos_id
        self._description: str = description
        
################################################################################
    @classmethod
    def new(cls: Type[R], bot: PartyBusBot, position: str, description: str) -> R:
        
        new_id = bot.database.insert.requirement(position, description)
        return cls(bot, new_id, position, description)
    
################################################################################
    @classmethod
    def load(cls: Type[R], bot: PartyBusBot, data: Tuple[str, str, str]) -> R:
        
        return cls(bot, *data)
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def parent_id(self) -> str:
        
        return self._parent_id
    
################################################################################
    @property
    def description(self) -> str:
        
        return self._description
    
################################################################################
    @property
    def select_option(self) -> SelectOption:
        
        label = self.description if len(self.description) <= 50 else f"{self.description[:47]}..."
        return SelectOption(label=label, value=self.id)
    
################################################################################
    def line_item(self, overrides: Dict[str, RequirementLevel]) -> str:

        emoji = (
            BotEmojis.Cross if self.id not in overrides else overrides[self.id].emoji
        )
        
        ret = f"{emoji} | {self.description} "    
        if self.parent_id == "0":
            ret += f"**(Global)**"
        ret += "\n"
        
        return ret
    
################################################################################
    def delete(self) -> None:
        
        self._state.database.delete.requirement(self)
        
################################################################################
