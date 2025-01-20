import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from utils.custom_cog import CustomCog
from database.base_model import BaseModel, Base


class Facts(CustomCog):
    def __init__(self, bot, logger=None):
        super().__init__(bot, logger)

    @app_commands.command(name="fact")
    async def cat_fact(self, interaction: discord.Interaction):
        """
        Get a random cat fact.

        Parameters
        ----------
        interaction : discord.Interaction

        """
        await interaction.response.defer(thinking=True)
        url = "https://catfact.ninja/fact"
        try:
            async with aiohttp.ClientSession() as session:
                self.logger.info(" - Getting cat fact...")
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        text = data["fact"]
                        self.logger.info(" - Delivering cat fact")
                    else:
                        text = "Something went wrong."
                        self.logger.error(" - Bad response.")
            self.logger.info(" - Fact delivered. Self-destructing in 15 seconds.")
        except Exception as e:
            text = f"Error: {e}"
            self.logger.error(f" - {text}")

        msg = await interaction.followup.send(text)
        await msg.delete(delay=15)
        self.log_command_end()


async def setup(bot: commands.Bot):
    BaseModel.initialize(Base)  # Ensure tables are created
    await bot.add_cog(Facts(bot))
