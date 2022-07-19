import os

import aiohttp
import discord
from discord.ext import commands
from typing import Union

from cogs.utils.context import Context


class Lady(commands.Bot):
    user: discord.ClientUser
    session: aiohttp.ClientSession

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, command_prefix="^")
        self.initial_extensions = (
            'cogs.updater',
            'cogs.log_review',
        )

    async def get_context(self, origin: Union[discord.Interaction, discord.Message], /, *, cls=Context) -> Context:
        return await super().get_context(origin, cls=cls)

    async def setup_hook(self):
        #self.background_task.start()
        self.session = aiohttp.ClientSession()
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_message(self, message: discord.Message) -> None:
        await self.process_commands(message)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f'Logged in as {self.user}')


if __name__ == "__main__":
    Lady().run(os.environ["DISCORD_SECRET"])

