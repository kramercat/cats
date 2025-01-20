import discord
from sqlalchemy import Column, Integer, String, DateTime
import utils.datetime_utils as datetime_utils
from database.base_model import BaseModel, Base


class Commands(Base, BaseModel):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True))
    guild_id = Column(String)
    guild_name = Column(String)
    user_id = Column(String)
    user_name = Column(String)
    command_name = Column(String)
    command_args = Column(String)
    channel_id = Column(String)
    channel_name = Column(String)

    @classmethod
    def log_command(cls, interaction: discord.Interaction):
        """Log a command interaction."""
        session = cls.db_manager.get_session()
        command = cls(
            date=datetime_utils.now(),
            guild_id=interaction.guild_id,
            guild_name=interaction.guild.name,
            user_id=interaction.user.id,
            user_name=interaction.user.name,
            command_name=interaction.command.name,
            command_args=str(interaction.command.parameters),
            channel_id=interaction.channel_id,
            channel_name=interaction.channel.name,
        )
        session.add(command)
        session.commit()
