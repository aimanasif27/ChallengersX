import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

from checkpost import check_linkedin_post, check_twitter_post
from mongo import insert_details
# Load environment variables from .env file
load_dotenv()
# Access the TOKEN environment variable
TOKEN = os.getenv('TOKEN')

# Define the intents you need
intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance with intents and command prefix
bot = commands.Bot(command_prefix='!cx ', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

# Command: Register
@bot.command()
async def register(ctx, *args):
    if not args:
        await ctx.send("You didn't provide an event.")
    else:
        event = ' '.join(args)
        # user = ctx.author
        # add_event(user.mention, event)

        user = ctx.author
        
        print(user)
        await ctx.send(f'{user}, We will be adding this functionality soon to register you for {event}!')
    
# Command: ndaysofcode
@bot.command()
async def _30daysofcode(ctx, *args):
    event = '#30daysofcode'
    if not args:
        await ctx.send("You didn't provide a link.")
    else:
        link = ' '.join(args)
        if link.startswith('https://www.linkedin.com') and check_linkedin_post(link):
            insert_details(ctx.author, event, link)
            await ctx.send("We noted your response!")
        elif link.startswith('https://twitter.com') and check_twitter_post(link):
            insert_details(ctx.author, event, link)
            await ctx.send("We noted your response!")
        else:
            await ctx.send("You didn't provide correct LinkedIn or Twitter post link!")

# Command: Help
@bot.command()
async def _help(ctx):
    await ctx.send('Use `!cx ndaysofcode <link>` to post your submission\nUse `!cx register <event_name>` to Register for the event')

# Error handler for CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!cx _help` to see available commands.")


bot.run(TOKEN)
