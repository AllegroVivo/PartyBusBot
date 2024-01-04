from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Trainee, TimeRange
    from Utils import Weekday, Hours, Timezone
################################################################################

__all__ = ("DatabaseInserter",)

################################################################################
class DatabaseInserter(DBWorkerBranch):
    """A utility class for inserting new records into the database."""

    def insert_position(self, name: str) -> str:
        """Inserts a new position into the database."""

        new_id = self.generate_id()
        
        with self.database as db:
            db.execute(
                "INSERT INTO positions (_id, name) VALUES (%s, %s);",
                (new_id, name)
            )
            
        return new_id

################################################################################
    def insert_new_requirement(self, position: str, description: str) -> str:

        new_id = self.generate_id()

        with self.database as db:
            db.execute(
                "INSERT INTO requirements (_id, position, description) "
                "VALUES (%s, %s, %s);",
                (new_id, position, description)
            )

        return new_id
    
################################################################################
    def insert_tuser_records(self, user_id: int) -> None:
        
        with self.database as db:
            db.execute(
                "INSERT INTO tusers (user_id) VALUES (%s);",
                (user_id,)
            )
            db.execute(
                "INSERT INTO tuser_config (user_id) VALUES (%s);",
                (user_id,)
            )
            db.execute(
                "INSERT INTO trainers (user_id) VALUES (%s);",
                (user_id,)
            )
            db.execute(
                "INSERT INTO trainees (user_id) VALUES (%s);",
                (user_id,)
            )
            
################################################################################
    def insert_trainer(self, user_id: int) -> str:
        """Inserts a new trainer into the database."""
        
        new_id = self.generate_id()
        
        with self.database as db:
            db.execute(
                "INSERT INTO trainers (_id, user_id, name, qualifications, trainees) "
                "VALUES (%s, %s, %s, %s, %s);",
                (new_id, user_id, None, [], [])
            )
            
        return new_id

################################################################################
    def insert_trainee(self, user_id: int) -> str:
        """Inserts a new trainee into the database."""
        
        new_id = self.generate_id()
        
        with self.database as db:
            db.execute(
                "INSERT INTO trainees (_id, user_id, name, trainings) "
                "VALUES (%s, %s, %s, %s);",
                (new_id, user_id, None, [])
            )
            
        return new_id
    
################################################################################
    def insert_new_qualification(self, user_id: int, pos_id: str, level: int) -> str:
        
        new_id = self.generate_id()
        
        with self.database as db:
            db.execute(
                "INSERT INTO qualifications (_id, user_id, position, level) "
                "VALUES (%s, %s, %s, %s);",
                (new_id, user_id, pos_id, level)
            )

        return new_id
        
################################################################################
    def insert_new_training(self, user_id: int, position: str) -> str:
            
        new_id = self.generate_id()
        
        with self.database as db:
            db.execute(
                "INSERT INTO trainings (_id, user_id, position) "
                "VALUES (%s, %s, %s);",
                (new_id, user_id, position)
            )
            
        return new_id
    
################################################################################
    def insert_requirement_override(self, training_id: str, requirement_id: str, level: int) -> None:
        
        with self.database as db:
            db.execute(
                "INSERT INTO requirement_overrides (training, requirement, level) "
                "VALUES (%s, %s, %s);",
                (training_id, requirement_id, level)
            )
            
################################################################################
    def insert_availability(self, user_id: int, day: int, start: int, end: Optional[int]) -> None:
        
        with self.database as db:
            db.execute(
                "INSERT INTO availability (user_id, day, start_time, end_time) "
                "VALUES (%s, %s, %s, %s);",
                (user_id, day, start, end)
            )
            
################################################################################
    
    position                = insert_position
    requirement             = insert_new_requirement
    tuser                   = insert_tuser_records
    trainer                 = insert_trainer
    trainee                 = insert_trainee
    qualification           = insert_new_qualification
    training                = insert_new_training
    requirement_override    = insert_requirement_override
    availability            = insert_availability
    
################################################################################
    