import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the TOKEN environment variable
TOKEN = os.getenv('TOKEN')

# Define the intents you need
intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance with intents and command prefix
bot = commands.Bot(command_prefix='!cx_', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

# Command: Hello
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
# Command: Ping
@bot.command()
async def ndaysofcode(ctx, *args):
    if not args:
        await ctx.send("You didn't provide a link.")
    else:
        sentence = ' '.join(args)
        response = f'You said: {sentence}'
        await ctx.send(response)

# Error handler for CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!help` to see available commands.")


bot.run(TOKEN)