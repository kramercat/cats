import discord
from discord.ext import commands
from discord import app_commands
from utils.custom_cog import CustomCog


class Treesync(CustomCog):
    def __init__(self, bot, logger=None):
        self.bot = bot
        self.logger = logger

    @app_commands.command(name="treesync")
    async def treesync(self, interaction: discord.Interaction):
        """
        Manually sync app commands.

        Parameters
        ----------
        interaction : discord.Interaction

        """
        await interaction.response.defer(thinking=True, ephemeral=True)
        msg = await interaction.followup.send(" > Syncing app commands...")
        await self.bot.tree.sync()
        await msg.edit(content=" > App commands synced. Self-destructing.")
        await msg.delete(delay=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Treesync(bot))
