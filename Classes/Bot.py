from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from discord import Attachment, Bot, Interaction, Role, User, TextChannel

from Classes.Positions import PositionManager
from Classes.Training import TrainingManager
from Utils.Database import Database

if TYPE_CHECKING:
    from Classes import Position
################################################################################

__all__ = ("PartyBusBot",)

################################################################################
class PartyBusBot(Bot):

    __slots__ = (
        "_image_dump",
        "training_manager",
        "position_manager",
        "database"
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._image_dump: TextChannel = None  # type: ignore
        
        self.database: Database = Database(self)
        
        self.training_manager: TrainingManager = TrainingManager(self)
        self.position_manager: PositionManager = PositionManager(self)

################################################################################
    async def load_all(self) -> None:

        print("Fetching image dump...")
        self._image_dump = await self.fetch_channel(991902526188302427)

        print("Asserting database structure...")
        self.database.assert_structure()
        
        print("Loading data from database...")
        data = self.database.load_all()
        
        await self.position_manager.load_all(data)
        print("Position Manager Loaded!")
        await self.training_manager.load_all(data)
        print("Training Manager Loaded!")

        print("Done!")

################################################################################
    async def dump_image(self, image: Attachment) -> str:

        file = await image.to_file()
        post = await self._image_dump.send(file=file)   # type: ignore

        return post.attachments[0].url

################################################################################
    async def add_position(self,  interaction: Interaction,  position_name: str) -> None:

        await self.position_manager.add_position(interaction, position_name)

################################################################################
    async def trainer_status(self, interaction: Interaction, user: User) -> None:
        
        await self.training_manager.trainer_status(interaction, user)
        
################################################################################
    async def tuser_status(self, interaction: Interaction) -> None:
        
        await self.training_manager.tuser_status(interaction)

################################################################################
    def get_position(self, pos_id: str) -> Optional[Position]:
        
        return self.position_manager.get_position(pos_id)

################################################################################
    async def position_status(self, interaction: Interaction, position: Optional[str]) -> None:
        
        await self.position_manager.position_status(interaction, position)

################################################################################
    async def update_training(self, interaction: Interaction, trainee: User) -> None:
        
        await self.training_manager.update_training(interaction, trainee)

################################################################################
    async def tuser_admin_status(self, interaction: Interaction, user: User) -> None:
        
        await self.training_manager.tuser_admin_status(interaction, user)

################################################################################
    async def post_signup_message(self, interaction: Interaction, channel: TextChannel) -> None:
        
        await self.training_manager.post_signup_message(interaction, channel)

################################################################################
