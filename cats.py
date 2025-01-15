import discord
import os
import logging
from customlogger import CustomLogger

# setup logging
discord_logger = CustomLogger(name='discord', log_level=logging.DEBUG)
http_logger = CustomLogger(name='discord.http', log_level=logging.INFO, log_to_console=False)
console_logger = CustomLogger(name='console', log_level=logging.DEBUG, log_to_file=False)

# Access the loggers and use them
discord_logger.get_logger().debug("This is a debug message for the discord logger")
http_logger.get_logger().info("HTTP request made")
console_logger.get_logger().info("Bot is running")

# configure discord bot parameters
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):

        await message.channel.send('Hello!')

client.run(
    token=os.getenv('TOKEN'),
    log_handler=None,
)
