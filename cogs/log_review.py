import discord
from discord.ext import commands


class LogReview(commands.Cog):
    LOG_REVIEW_CHANNEL_ID = 894792867736866816
    FOUR_HORSEMEN = 894792866814111808

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Loaded {__class__}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == LogReview.LOG_REVIEW_CHANNEL_ID:
            if message.author.get_role(LogReview.FOUR_HORSEMEN) and message.content == "janny":
                await message.channel.purge(oldest_first=True, check=lambda m: not m.flags.has_thread)
                return
            # elif message.author.get_role(FOUR_HORSEMEN) and message.content == "purge":
            #     await message.channel.purge(oldest_first=True)
            #     for thread in message.channel.threads:
            #         await thread.archive()
            #     return

            if message.author == self.bot.user:
                await message.delete(delay=6)
                return

            text: str = message.content
            if text.startswith("https://classic.warcraftlogs.com/reports/") and (len(text) <= 57 or text[57] in ('#', '/', ' ')):
                await message.create_thread(name=f"Review for {message.author.display_name}")
                return

            if not message.author.get_role(LogReview.FOUR_HORSEMEN):
                await message.delete(delay=3)
                await message.channel.send("Please begin your post with a valid warcraft logs report to start a review:\n"
                                       "https://classic.warcraftlogs.com/reports/1234567890abcdef")
            return


async def setup(bot):
    await bot.add_cog(LogReview(bot))