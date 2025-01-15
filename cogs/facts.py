import discord
from discord.ext import commands
from discord import app_commands
import aiohttp


class Facts(commands.Cog):
    def __init__(self, bot, logger=None):
        self.bot = bot
        self.logger = logger

    @app_commands.command(name="fact")
    async def cat_fact(self, interaction: discord.Interaction):
        """
        Get a random cat fact.

        Parameters
        ----------
        interaction : discord.Interaction

        """
        self.logger.info(
            f"Guild ({interaction.guild_id}) ({interaction.user}) called {__name__}"
        )
        url = "https://catfact.ninja/fact"
        try:
            async with aiohttp.ClientSession() as session:
                self.logger.info(" > Getting cat fact...")
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        cat_fact = data["fact"]
                        await interaction.response.send_message(
                            cat_fact, delete_after=60
                        )
                        self.logger.info(" > Delivering cat fact")
                    else:
                        await interaction.response.send_message(
                            "Something went wrong.", delete_after=10
                        )
                        self.logger.error(" > Bad response.")
        except Exception as e:
            await interaction.response.send_message(f"Error.", delete_after=10)
            self.logger.error(f" > Error: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Facts(bot))
