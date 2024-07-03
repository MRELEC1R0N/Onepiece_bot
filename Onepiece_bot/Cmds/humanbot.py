import discord
from discord.ext import commands
import google.generativeai as genai
from Settings import Ai_api

# Replace these with your actual API key and other settings
api_key = Ai_api

genai.configure(api_key= api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

class GeminiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gemini(self, ctx, *, prompt):
        """Interacts with Gemini AI using a given prompt."""

        # Send a request to the Gemini API with the user's prompt
        response = model.start_chat().send_message(prompt)        
        # Extract the AI's response

        # Send the AI's response back to the user in Discord
        await ctx.send(response.text)

def setup(bot):
    bot.add_cog(GeminiCog(bot))
