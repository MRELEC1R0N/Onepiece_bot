import discord
from discord.ext import commands
from database import users
from supportfuntions.generate import generate_data  # Import your AI generation function
import  json

class UserProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_profiles = users

    async def get_user_input(self, ctx, prompt):
        await ctx.send(f"**{prompt}**")
        response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
        return response.content if response.content.lower() != 'na' else None



    async def generate_character_details(self, character_info):
        prompt = f"""
        You are a powerful AI model that generates detailed and engaging character profiles for a pirate-themed gamei on discord.
        

        Here is a character profile given by the user as he sees fit:

        Name: {character_info.get('name', 'N/A')}
        Alias: {character_info.get('alias', 'N/A')}
        Combat Skills: {character_info.get('combat_skills', 'N/A')}
        Personality: {character_info.get('personality', 'N/A')}
        Backstory: {character_info.get('backstory', 'N/A')}
        Goals: {character_info.get('goals', 'N/A')}
        Quirks: {character_info.get('quirks', 'N/A')}

        Based on the above information, please generate(if its N/A) the or improve the details for this character keeping this in mind :
    
        1. Fill in any missing details (Combat Skills, Personality, Backstory, Goals, Quirks).
        2. Detailed description of the character's appearance.
        3. Additional backstory details that flesh out their history and experiences.
        4. Ideas for interesting quests or missions the character could undertake.
        5. Any special abilities or unique traits the character might possess that can be used in the game ( its a cli based game).     6. Do not change the name , alias 
        generate this information in json format as it will be stored on mongodb for further usage
        """

        # Call the generate_data function to interact with the AI model
        response = generate_data(prompt)
        return response




     
    @commands.command(name='create_profile')
    async def create_profile(self, ctx):
        user_id = ctx.author.id
        user = self.user_profiles.find_one({'user_id': user_id})
        if user:
            await ctx.send("You already have a profile!")
            return

        await ctx.send("# Enter the Details to register your character in the game")

        name = await self.get_user_input(ctx, "Please enter your character's name:")
        alias = await self.get_user_input(ctx, "Please enter any alias or epithet for your character (optional, type 'NA' to leave empty):")
        combat_skills = await self.get_user_input(ctx, "Please enter your character's combat skills (optional, type 'NA' to leave empty):")
        personality = await self.get_user_input(ctx, "Please enter your character's personality traits (optional, type 'NA' to leave empty):")
        backstory = await self.get_user_input(ctx, "Please enter your character's backstory (optional, type 'NA' to leave empty):")
        goals = await self.get_user_input(ctx, "What are your character's goals and ambitions as a pirate? Describe them (optional, type 'NA' to leave empty):")
        quirks = await self.get_user_input(ctx, "Share any quirks, habits, or preferences your character has (optional, type 'NA' to leave empty):")

        character_info = {
        'name': name,
        'alias': alias,
        'combat_skills': combat_skills,
        'personality': personality,
        'backstory': backstory,
        'goals': goals,
        'quirks': quirks
    }


    # Generate additional character details using the AI model
        additional_details = await self.generate_character_details(character_info)

    # Extract JSON content from the AI response
        starting_index = additional_details.find("{")
        ending_index = additional_details.rfind("}")
        details = additional_details[starting_index:ending_index+1]

        try:
            
            data = json.loads(details)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            await ctx.send("There was an error generating the character details. Please try again.")
            return

    # Combine character info with additional details
        full_character_profile = {"_id": user_id, **data, 'bounty': 0}

    # Save the full character profile to the database
        self.user_profiles.insert_one(full_character_profile)

        await ctx.send(f"Profile created! Your name is {name}, and your current bounty is {full_character_profile['bounty']}.")

        await ctx.send("Here are your character's details:")
        embed = discord.Embed(title=f"{full_character_profile['name']} ({full_character_profile['alias']})", color=discord.Color.blue())
        embed.add_field(name="Combat Skills", value=full_character_profile.get('combat_skills', 'N/A'), inline=False)
        embed.add_field(name="Personality", value=full_character_profile.get('personality', 'N/A'), inline=False)
        embed.add_field(name="Backstory", value=full_character_profile.get('backstory', 'N/A'), inline=False)
        embed.add_field(name="Goals", value=full_character_profile.get('goals', 'N/A'), inline=False)
        embed.add_field(name="Quirks", value=full_character_profile.get('quirks', 'N/A'), inline=False)
        embed.add_field(name="Appearance", value=full_character_profile.get('appearance', 'N/A'), inline=False)
        embed.add_field(name="Extra Backstory", value=full_character_profile.get('additionalBackstory', 'N/A'), inline=False)
        embed.add_field(name="Notable Battles", value=full_character_profile.get('Notable Battles', 'N/A'), inline=False)
        embed.add_field(name="Quests", value=full_character_profile.get('quests', 'N/A'), inline=False)
        embed.add_field(name="Special Abilities", value=full_character_profile.get('specialAbilities', 'N/A'), inline=False)
        embed.add_field(name="Unique Traits", value=full_character_profile.get('Unique Traits', 'N/A'), inline=False)

        await ctx.send(embed=embed)


    @commands.command(name='view_profile')
    async def view_profile(self, ctx):
        user_id = ctx.author.id
        user = self.user_profiles.find_one({'_id': user_id})
        if not user:
            await ctx.send("You don't have a profile yet. Use the `create_profile` command to create one.")
            return

        embed = discord.Embed(title=f"{ctx.author.name}'s Pirate Profile", color=0xffcc00)
        for key, value in user.items():
            if key != 'user_id' and value:
                embed.add_field(name=key.replace('_', ' ').capitalize(), value=value, inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserProfileCog(bot))





'''
    Creating interesting characters for your One Piece Discord bot game involves several key elements to make battles, quests, and interactions engaging. Here are some ideas on what information you might consider including for each character:

1. **Name and Alias**: Every pirate needs a distinctive name and possibly an alias or epithet.

2. **Bounty**: A measure of their notoriety and strength, which can affect how other characters perceive them and the challenges they face.

3. **Devil Fruit Ability (if any)**: In the One Piece universe, Devil Fruits grant unique powers. Include details about the character's Devil Fruit abilities, if applicable.

4. **Combat Skills**: Specify their combat style, weapon proficiency, or martial arts techniques. This could influence battle outcomes and strategies.

5. **Personality Traits**: Describe their temperament, quirks, and moral code. This can affect interactions with other characters and decisions during quests.

6. **Backstory**: Provide a backstory that explains their motivations, goals, and past experiences. This gives depth to the character and can drive quest narratives.

7. **Special Items or Treasures**: Unique items or treasures they possess, which could be sought after or used strategically in battles.

8. **Affiliations**: Mention any alliances, rivalries, or past associations with other characters or factions. This can create complex social dynamics and plot twists.

9. **Goals and Ambitions**: Define what the character wants to achieve in the world of your Discord game. This can drive quest objectives and character development over time.

10. **Quirks and Habits**: Small details like favorite foods, superstitions, or habits that make the character memorable and add depth.

By fleshing out these aspects for each character, you can create a rich and immersive experience where players can interact, battle, form alliances, and uncover stories across different servers in your Discord bot game. '''   
