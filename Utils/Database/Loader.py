from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Tuple, List, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader(DBWorkerBranch):
    """A utility class for loading data from the database."""

    def load_all(self) -> Dict[str, Any]:
        """Performs all sub-loaders and returns a dictionary of their results."""

        return {
            "positions": self.load_positions(),
            "requirements": self.load_requirements(),
            "tusers": self.load_tusers(),
            "configs": self.load_tuser_configs(),
            "availabilities": self.load_availabilities(),
            "trainers": self.load_trainers(),
            "trainees": self.load_trainees(),
            "qualifications": self.load_qualifications(),
            "trainings": self.load_trainings(),
            "requirement_overrides": self.load_requirement_overrides(),
            "messages": self.load_messages(),
        }

################################################################################
    def load_positions(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all positions from the database."""

        with self.database as db:
            db.execute("SELECT * FROM positions;")
            return db.fetchall()

################################################################################
    def load_requirements(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all requirements from the database."""

        with self.database as db:
            db.execute("SELECT * FROM requirements;")
            return db.fetchall()
        
################################################################################
    def load_tusers(self) -> Tuple[Tuple[Any, ...], ...]:
    
        with self.database as db:
            db.execute("SELECT * FROM tusers;")
            return db.fetchall()

################################################################################
    def load_tuser_configs(self) -> Tuple[Tuple[Any, ...]]:
        """Loads all trainee configs from the database."""

        with self.database as db:
            db.execute("SELECT * FROM tuser_config;")
            return db.fetchall()

################################################################################
    def load_availabilities(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all availabilities from the database."""

        with self.database as db:
            db.execute("SELECT * FROM availability;")
            return db.fetchall()
        
################################################################################
    def load_trainers(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all trainers from the database."""

        with self.database as db:
            db.execute("SELECT * FROM trainers;")
            return db.fetchall()            
        
################################################################################
    def load_trainees(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all trainees from the database."""

        with self.database as db:
            db.execute("SELECT * FROM trainees;")
            return db.fetchall()
        
################################################################################
    def load_qualifications(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all qualifications from the database."""

        with self.database as db:
            db.execute("SELECT * FROM qualifications;")
            return db.fetchall()
            
################################################################################
    def load_trainings(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all trainings from the database."""

        with self.database as db:
            db.execute("SELECT * FROM trainings;")
            return db.fetchall()
        
################################################################################
    def load_requirement_overrides(self) -> Tuple[Tuple[Any, ...], ...]:
        """Loads all requirement overrides from the database."""

        with self.database as db:
            db.execute("SELECT * FROM requirement_overrides;")
            return db.fetchall()
        
################################################################################
    def load_messages(self) -> Dict[str, Tuple[Any, ...]]:
        """Loads all messages from the database."""

        with self.database as db:
            db.execute("SELECT * FROM messages;")
            data = db.fetchall()
            
        return {
            "trainer_message": data[0][1:3],
        }
        
################################################################################
            