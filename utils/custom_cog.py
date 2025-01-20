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

    def log_header(self, message):
        self.logger.info("--> " + message)

    def log_command_start(self, interaction: discord.Interaction):
        self.log_header(
            f"Guild ({interaction.guild_id}) ({interaction.user}) called /{interaction.command.name}"
        )

    def log_command_end(self):
        self.log_header(f"Command complete.")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        self.log_command_start(interaction)
        # Insert a record into the command log
        Commands.log_command(interaction)
        return True
