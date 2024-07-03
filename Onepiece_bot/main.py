import tracemalloc
import discord 
from discord.ext import commands
import Settings

# Set up the logger
logger = Settings.logging.getLogger("bot")
2
# Define the function to run the bot
def run():
    intents = discord.Intents.all()
    # intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    # Load all cogs on bot ready
    async def load_cogs():
        for cog_file in Settings.CMDS_DIR.glob("*.py"):
            if cog_file.is_file():
                bot.load_extension(f"Cmds.{cog_file.stem}")
                logger.info(f"Loaded {cog_file.stem}")

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        await load_cogs()

    for cmd in ['load', 'unload', 'reload']:
        @bot.command(name=  cmd)
        async def _cmd(ctx, cog: str):
            try:
                await getattr(bot, f'{cmd}_extension')(f"Cmds.{cog.lower()}")
                await ctx.send(f'Done {cmd}ing')
            except Exception as e:
                await ctx.send(f'Error: {e}')

    tracemalloc.start()
    bot.run(Settings.Discord_api)

if __name__ == "__main__":
    run()
