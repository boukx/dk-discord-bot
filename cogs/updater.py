import asyncio
import os

from aiohttp import web
import hmac
from git import Repo

from discord.ext import commands


class Updater(commands.Cog):
    GITHUB_SECRET = os.environ["GITHUB_SECRET"]
    REPO_PATH = os.environ["REPO_PATH"]

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Loaded {__class__}")

    async def webserver(self):
        async def github_webhook_endpoint(request):
            signature = request.headers.get("X-Hub-Signature")
            sha, signature = signature.split('=')

            # Create local hash of payload
            digest = hmac.new(Updater.GITHUB_SECRET.encode(), request.data, digestmod='sha1').hexdigest()

            # Verify signature
            if hmac.compare_digest(signature, "sha1=" + digest):
                repo = Repo(self.REPO_PATH)
                origin = repo.remotes.origin
                origin.pull('--rebase')

                commit = request.json['after'][0:6]
                print(f'Repository updated with commit {commit}')

            return web.Response(text="thanks")

        app = web.Application()
        app.router.add_post('/github', github_webhook_endpoint)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '127.0.0.1', 8080)
        await self.bot.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


async def setup(bot):
    updater = Updater(bot)
    await bot.add_cog(updater)
    await bot.loop.create_task(updater.webserver())


