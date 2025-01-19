import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from utils.custom_cog import CustomCog


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
        url = "https://catfact.ninja/fact"
        try:
            async with aiohttp.ClientSession() as session:
                self.logger.info(" > Getting cat fact...")
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        cat_fact = data["fact"]
                        msg = await interaction.response.send_message(cat_fact)
                        await msg.delete(delay=60)
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
