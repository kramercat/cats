import discord
from database.base_model import BaseModel
import utils.datetime_utils as datetime_utils


class Commands(BaseModel):
    class Meta:
        table = "commands"
        columns = {
            "date": "DATETIME",
            "guild_id": "TEXT",
            "guild_name": "TEXT",
            "user_id": "TEXT",
            "user_name": "TEXT",
            "command_name": "TEXT",
            "command_args": "TEXT",
            "channel_id": "TEXT",
            "channel_name": "TEXT",
        }

    @classmethod
    def log_command(cls, interaction: discord.Interaction):
        """Log a command interaction."""
        values = {
            "date": datetime_utils.now(),
            "guild_id": interaction.guild_id,
            "guild_name": interaction.guild.name,
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "command_name": interaction.command.name,
            "command_args": str(interaction.command.parameters),
            "channel_id": interaction.channel_id,
            "channel_name": interaction.channel.name,
        }
        cls.create(values)
