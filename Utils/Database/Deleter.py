from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Requirement, Training, Qualification
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseDeleter",)

################################################################################
class DatabaseDeleter(DBWorkerBranch):
    """A utility class for deleting data from the database."""

    def delete_requirement(self, req: Requirement) -> None:

        with self.database as db:
            db.execute(
                "DELETE FROM requirements WHERE _id = %s;",
                (req.id,)
            )
            
################################################################################
    def delete_training(self, training: Training) -> None:
    
        with self.database as db:
            db.execute(
                "DELETE FROM trainings WHERE _id = %s;",
                (training.id,)
            )
            
        # self.delete_requirement_overrides(training.id, training.requirement_overrides)
    
################################################################################
    def delete_requirement_overrides(self, training_id: str, overrides: Dict[str, RequirementLevel]) -> None:
        
        with self.database as db:
            for req_id, _ in overrides.items():
                db.execute(
                    "DELETE FROM requirement_overrides WHERE training = %s "
                    "AND requirement = %s;",
                    (training_id, req_id)
                )
    
################################################################################
    def delete_qualification(self, qualification: Qualification) -> None:
    
        with self.database as db:
            db.execute(
                "DELETE FROM qualifications WHERE _id = %s;",
                (qualification.id,)
            )
            
################################################################################

    requirement     = delete_requirement
    training        = delete_training
    qualification   = delete_qualification

################################################################################
