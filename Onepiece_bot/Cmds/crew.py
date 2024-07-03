import discord
from discord.ext import commands
from database import  crew

class CrewManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crews = crew

    @commands.command(name='create_crew')
    async def create_crew(self, ctx, *, name: str):
        user_id = ctx.author.id
        crew = self.crews.find_one({'members.user_id': user_id})
        if crew:
            await ctx.send("You already belong to a crew. Leave your current crew first to create a new one.")
            return

        new_crew = {
            'name': name,
            'bounty': 0,
            'members': [
                {'user_id': user_id, 'role': 'Captain'}
            ]
        }
        self.crews.insert_one(new_crew)
        await ctx.send(f"Crew '{name}' created! You are now the Captain.")

    @commands.command(name='join_crew')
    async def join_crew(self, ctx, crew_id: str):
        user_id = ctx.author.id
        crew = self.crews.find_one({'_id': ObjectId(crew_id)})
        if not crew:
            await ctx.send("Invalid crew ID.")
            return

        if any(member['user_id'] == user_id for member in crew['members']):
            await ctx.send("You already belong to this crew.")
            return

        self.crews.update_one(
            {'_id': ObjectId(crew_id)},
            {'$push': {'members': {'user_id': user_id, 'role': 'Member'}}}
        )
        await ctx.send(f"You have joined the {crew['name']} crew!")

    @commands.command(name='leave_crew')
    async def leave_crew(self, ctx):
        user_id = ctx.author.id
        crew = self.crews.find_one({'members.user_id': user_id})
        if not crew:
            await ctx.send("You don't belong to any crew.")
            return

        self.crews.update_one(
            {'_id': crew['_id']},
            {'$pull': {'members': {'user_id': user_id}}}
        )
        await ctx.send(f"You have left the {crew['name']} crew.")

    @commands.command(name='crew_info')
    async def crew_info(self, ctx, crew_id: str = None):
        user_id = ctx.author.id
        if crew_id is None:
            crew = self.crews.find_one({'members.user_id': user_id})
            if not crew:
                await ctx.send("You don't belong to any crew.")
                return
        else:
            crew = self.crews.find_one({'_id': ObjectId(crew_id)})
            if not crew:
                await ctx.send("Invalid crew ID.")
                return

        member_count = len(crew['members'])
        embed = discord.Embed(title=f"{crew['name']} Crew Info", color=0xffcc00)
        embed.add_field(name="Crew Name", value=crew['name'], inline=True)
        embed.add_field(name="Crew Bounty", value=f"{crew['bounty']:,}", inline=True)
        embed.add_field(name="Members", value=member_count, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CrewManagementCog(bot))

