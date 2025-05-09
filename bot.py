"""This is the main file for the bot."""
from typing import Any
import os
import traceback
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import ExtensionError
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.message_content = True
intents.guilds = True

async def cog_loader(bot_instance: commands.Bot) -> None:
    """This function loads all cogs in the cogs folder."""
    await bot_instance.load_extension("jishaku")
    for file in os.listdir('./cogs'):
        if file.endswith('.py') and file != '__init__.py':
            cog_name = file[:-3]
            try:
                await bot_instance.load_extension(f'cogs.{cog_name}')
                print(f'Successfully loaded {cog_name}')
            except ExtensionError as e:
                print(f'Failed to load cog {cog_name}: {str(e)}')
                print(traceback.format_exc())

class FangsterBot(commands.Bot): # type: ignore
    """The main bot class."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def on_ready(self) -> None:
        """This function is called when the bot is ready."""
        print(f"Logged in as {self.user.name}")
        print("Ready to log all reactions!")

    async def setup_hook(self) -> None:
        """This function is called when the bot starts."""
        await cog_loader(self)

bot = FangsterBot(command_prefix="uwu ", intents=intents, message_cache_size=1000)

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
