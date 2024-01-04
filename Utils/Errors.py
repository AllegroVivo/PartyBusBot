from __future__ import annotations

from datetime import datetime
from typing import Optional

from discord import Embed, Colour, User

from Assets import BotImages
################################################################################

__all__ = (
    "PositionExistsError",
    "TrainerExistsError",
    "TrainerNotFoundError",
    "TraineeExistsError",
    "TraineeNotFoundError",
    "RoleNotFoundError",
    "PositionNotFoundError",
    "InvalidRoleIDError",
    "InvalidNumberError",
    "TraineeMissingError",
    "UnqualifiedError",
)

################################################################################
class ErrorMessage(Embed):
    """A subclassed Discord embed object acting as an error message."""

    def __init__(
        self,
        *,
        title: str,
        message: str,
        solution: str,
        description: Optional[str] = None
    ):

        super().__init__(
            title=title,
            description=description,
            colour=Colour.red()
        )

        self.add_field(
            name="What Happened?",
            value=message,
            inline=True,
        )

        self.add_field(
            name="How to Fix?",
            value=solution,
            inline=True
        )

        self.timestamp = datetime.now()
        self.set_thumbnail(url=BotImages.ErrorFrog)
    
################################################################################
class PositionExistsError(ErrorMessage):
    
    def __init__(self, position_name: str):
        
        super().__init__(
            title="Position Exists",
            message=f"The position `{position_name}` already exists.",
            solution=f"Try a different name for the position."
        )
        
################################################################################
class PositionNotFoundError(ErrorMessage):
        
    def __init__(self, position_name: str):
        
        super().__init__(
            title="Position Not Found",
            message=f"The position `{position_name}` was not found.",
            solution=f"Try a different name for the position."
        )
            
################################################################################
class TrainerExistsError(ErrorMessage):
    
    def __init__(self, user: User):
        
        super().__init__(
            title="Trainer Exists",
            message=f"The trainer {user.mention} already exists.",
            solution=f"Try a different user."
        )
        
################################################################################
class TrainerNotFoundError(ErrorMessage):
    
    def __init__(self, user: User):
        
        super().__init__(
            title="Trainer Not Found",
            message=f"The user {user.mention} has not been registered as a trainer.",
            solution=f"Try a different user."
        )
        
################################################################################
class TraineeExistsError(ErrorMessage):
    
    def __init__(self, user: User):
        
        super().__init__(
            title="Trainee Exists",
            message=f"The user {user.mention} already exists as a trainee.",
            solution=f"Try a different user."
        )
        
################################################################################
class TraineeNotFoundError(ErrorMessage):
    
    def __init__(self, user: User):
        
        super().__init__(
            title="Trainee Not Found",
            message=f"The user {user.mention} has not been registered as a trainee.",
            solution=f"Try a different user."
        )
        
################################################################################
class RoleNotFoundError(ErrorMessage):
    
    def __init__(self, role: str):
        
        super().__init__(
            title="Role Not Found",
            message=f"A server role with the signature `{role}` was not found.",
            solution=f"Are you sure you mentioned an existing role."
        )
        
################################################################################
class InvalidRoleIDError(ErrorMessage):
    
    def __init__(self, role: str):
        
        super().__init__(
            title="Invalid Role ID",
            message=f"A role with the ID `{role}` was not located.",
            solution=f"Are you sure you mentioned an existing role."
        )
        
################################################################################
class InvalidNumberError(ErrorMessage):
    
    def __init__(self, number: str):
        
        super().__init__(
            title="Invalid Number",
            message=f"The value `{number}` is not a valid number.",
            solution=f"Are you sure you entered a number?"
        )
        
################################################################################
class TraineeMissingError(ErrorMessage):
    
    def __init__(self, user: int):
        
        super().__init__(
            title="Trainee Missing",
            message=f"The a user with ID#: {user} is not registered as a trainee.",
            solution=f"Consult management to force a post update on this message."
        )
        
################################################################################
class UnqualifiedError(ErrorMessage):
    
    def __init__(self, user: User):
        
        super().__init__(
            title="Unqualified :(",
            message=f"The user {user.mention} is not qualified to train this position.",
            solution=f"Consult management to earn qualifications to train, or select another trainee."
        )
        
################################################################################
