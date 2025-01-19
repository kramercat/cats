import discord
from discord.ext import commands
from utils.logger_utils import CustomLogger
import logging

from database.models.commands import Commands


class CustomCog(commands.Cog):
    def __init__(self, bot, logger=None):
        self.bot = bot
        self.logger = logger or CustomLogger(
            name="command_logger", log_level=logging.DEBUG
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        self.logger.info(
            f"Guild ({interaction.guild_id}) ({interaction.user}) called {interaction.command.name}"
        )
        # Insert a record into the command log
        Commands.log_command(interaction)
        return True
