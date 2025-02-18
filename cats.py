import discord
from discord.ext import commands
import os
import logging
import pathlib
from utils.logger_utils import CustomLogger
from database.db_manager import DatabaseManager
from database.models.guilds import Guilds


# setup logging
pathlib.Path("logs").mkdir(exist_ok=True)
discord_logger = CustomLogger(name="discord", log_level=logging.DEBUG)
http_logger = CustomLogger(
    name="discord.http", log_level=logging.DEBUG, log_to_console=False
)
logging.getLogger("discord.http").setLevel(logging.DEBUG)
logging.getLogger("discord.http").addHandler(http_logger.file_handler())
console_logger = CustomLogger(name="console", log_level=logging.DEBUG, log_to_file=True)

# configure discord bot parameters
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="Herding cats.")


@bot.event
async def load_cogs():
    """
    Load all cogs from the 'cogs' directory. Only files that match the pattern
    '[a-z]+.py' are considered valid and will be loaded.

    Logs a message for any file that doesn't meet the naming convention.
    """
    cogs = os.listdir("cogs")
    cogs_ignore = ["__pycache__"]
    for cog in cogs:
        if cog.endswith(".py"):
            cog_name = cog[:-3]

            cog_log_folder = f"logs/{cog_name}"
            pathlib.Path(cog_log_folder).mkdir(exist_ok=True)
            # cog specific logger
            cog_logger = CustomLogger(
                name=cog_name,
                log_level=logging.DEBUG,
                log_file=f"logs/{cog_name}/{cog_name}.log",
            )

            try:
                await bot.load_extension(f"cogs.{cog_name}")
                discord_logger.info(f"Loaded extension: ({cog_name})")
                cog = bot.get_cog(cog_name.capitalize())
                if cog:
                    # attach logger
                    setattr(cog, "logger", cog_logger)
                    discord_logger.info(f" - Logger attached")

            except Exception as e:
                discord_logger.error(e)
        else:
            if cog in cogs_ignore:
                continue
            discord_logger.info(
                f"Cog ({cog}) failed name check. Check that formatting is all lower case (ex: abc.py)."
            )


@bot.event
async def on_guild_join(guild):
    discord_logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    # Insert the new guild into the database
    Guilds.insert_guild(guild.id, guild.name)


@bot.event
async def on_guild_remove(guild):
    discord_logger.info(f"Left guild: {guild.name} (ID: {guild.id})")

    # Update the guild's leave_date in the database
    Guilds.update_guild_leave_date(guild.id)


@bot.event
async def on_ready():
    discord_logger.info(f"----- [Logged in as {bot.user}] -----")
    await load_cogs()
    discord_logger.info(f"----- [Loading cogs complete] -----")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("$hello"):

        msg = await message.channel.send("Hello!")
        await msg.delete(delay=60)


bot.run(
    token=os.getenv("TOKEN"),
    log_handler=None,
)
