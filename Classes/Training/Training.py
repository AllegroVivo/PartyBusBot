from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar, Any, Dict

from discord import EmbedField

from Assets import BotEmojis
from Utils import RequirementLevel

if TYPE_CHECKING:
    from Classes import Position, Trainee, Trainer, TrainingManager, PartyBusBot
################################################################################

__all__ = ("Training", )

T = TypeVar("T", bound="Training")

################################################################################
class Training:
    
    __slots__ = (
        "_id",
        "_position",
        "_trainee",
        "_trainer",
        "_overrides",
    )
    
################################################################################
    def __init__(
        self, 
        _id: str,
        position: Position,
        trainee: Trainee,
        trainer: Optional[Trainer] = None,
        overrides: Optional[Dict[str, RequirementLevel]] = None
    ) -> None:
        
        self._id: str = _id
        self._position: Position = position
        
        self._trainee: Trainee = trainee
        self._trainer: Optional[Trainer] = trainer
        
        self._overrides: Dict[str, RequirementLevel] = overrides or {}
    
################################################################################
    def __eq__(self, other: Training) -> bool:
        
        return self._id == other.id
        
################################################################################    
    @classmethod
    def new(cls: Type[T], trainee: Trainee, position_id: str) -> T:
        
        bot = trainee.bot
        new_id = bot.database.insert.training(trainee.user_id, position_id)
        position = bot.position_manager.get_position(position_id)
        
        return cls(new_id, position, trainee)
    
################################################################################
    @classmethod
    def load(
        cls: Type[T], 
        parent: Trainee, 
        data: Tuple[Any, ...]
    ) -> T:
        
        mgr = parent.bot.training_manager
        
        position = mgr.bot.get_position(data[2])
        # trainer = mgr.get_trainer(data[3])
        
        # overrides = {
        #     requirement_id: RequirementLevel(level)
        #     for _, requirement_id, level in override_data
        # }
        
        return cls(data[0], position, parent, None, {})
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._trainee.bot
    
################################################################################
    @property 
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def position(self) -> Position:
        
        return self._position
    
################################################################################
    @property
    def trainee(self) -> Trainee:
        
        return self._trainee
    
################################################################################
    @property
    def trainer(self) -> Optional[Trainer]:
        
        return self._trainer
    
################################################################################        
    @trainer.setter
    def trainer(self, value: Optional[Trainer]) -> None:
        
        self._trainer = value
        self.update()
        
################################################################################
    @property
    def requirement_overrides(self) -> Dict[str, RequirementLevel]:
        
        return self._overrides
    
################################################################################
    @property
    def embed_field(self) -> EmbedField:

        all_requirements = (
            self.position.requirements + 
            self._trainee.bot.position_manager.global_requirements
        )
        field_value = ""
        for req in all_requirements:
            field_value += req.line_item(self.requirement_overrides)
    
        return EmbedField(
            name=self.position.name,
            value=field_value,
            inline=True
        )
    
################################################################################
    def line_item(self, overrides: Dict[str, RequirementLevel]) -> str:
        
        completed_reqs = []
        inprogress_reqs = []
        incomplete_reqs = []
        waived_reqs = []
        
        for req in self.position.requirements:
            if req.id in overrides.keys():
                match overrides[req.id]:
                    case RequirementLevel.Complete:
                        completed_reqs.append(req)
                    case RequirementLevel.InProgress:
                        inprogress_reqs.append(req)
                    case RequirementLevel.Incomplete:
                        incomplete_reqs.append(req)
                    case RequirementLevel.Waived:
                        waived_reqs.append(req)
            
        additional = "\n"        
        if len(completed_reqs) > 0:
            additional += f"*Completed:"

        return (
            f"{self.position.name}"
            f"{additional}"
        )
    
################################################################################
    def add_requirement_override(self, requirement_id: str, level: RequirementLevel) -> None:
        
        self._overrides[requirement_id] = level
        self.update()
        
################################################################################
    def delete(self) -> None:
        
        self.bot.database.delete.training(self)
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.training(self)
        
################################################################################
