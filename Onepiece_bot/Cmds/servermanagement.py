from supportfuntions.island_generator import generate_island
from database import islands
import discord
from discord.ext import commands

class ServerManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_island')
    @commands.is_owner()
    async def create_island(self, ctx):
        guild = ctx.guild
        island_data = generate_island(guild)
        island = islands.find_one({'name': island_data['name']})
        if not island:
            islands.insert_one(island_data)
            await ctx.send(f"Island '{island_data['name']}' created successfully!")
        else:
            await ctx.send(f"Island '{island_data['name']}' already exists.")

    @commands.command(name='remove_island')
    async def remove_island(self, ctx):
        guild = ctx.guild
        island = islands.find_one({'name': guild.name})
        if island:
            islands.delete_one({'_id': guild.id})
            await ctx.send(f"Island '{guild.name}' removed successfully!")
        else:
            await ctx.send(f"No island found for '{guild.name}'.") 

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        island_data = generate_island(guild)
        island = islands.find_one({'name': island_data['name']})
        if not island:
            islands.insert_one(island_data)
            print(f"Created island: {island_data['name']}")
        else:
            print(f"Island '{island_data['name']}' already exists.")

def setup(bot):
    bot.add_cog(ServerManagementCog(bot))

