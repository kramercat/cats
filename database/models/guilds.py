from sqlalchemy import Column, Integer, String, DateTime
import utils.datetime_utils as datetime_utils
from database.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Guilds(Base, BaseModel):
    __tablename__ = "guilds"
    guild_id = Column(Integer, primary_key=True)
    guild_name = Column(String)
    join_date = Column(DateTime(timezone=True))
    leave_date = Column(DateTime(timezone=True), nullable=True)

    commands = relationship("Commands", back_populates="guild")

    @classmethod
    def insert_guild(cls, guild_id: int, guild_name: str):
        """Insert a new guild into the guilds table."""
        session = cls.db_manager.get_session()
        guild = cls(
            guild_id=guild_id, guild_name=guild_name, join_date=datetime_utils.now()
        )
        session.add(guild)
        session.commit()

    @classmethod
    def update_guild_leave_date(cls, guild_id: int):
        """Update the leave date for a guild."""
        session = cls.db_manager.get_session()
        guild = session.query(cls).filter_by(guild_id=guild_id).first()
        if guild:
            guild.leave_date = datetime_utils.now()
            session.commit()
