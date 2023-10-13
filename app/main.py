import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

from checkpost import check_linkedin_post, check_twitter_post

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
        sentence = ' '.join(args)
        await ctx.send(f'We will be adding this functionality soon to register you for {sentence}!')
    
# Command: ndaysofcode
@bot.command()
async def ndaysofcode(ctx, *args):
    if not args:
        await ctx.send("You didn't provide a link.")
    else:
        link = ' '.join(args)
        if link.startswith('https://www.linkedin.com') and check_linkedin_post(link):
                await ctx.send("We noted your response!")
        elif link.startswith('https://twitter.com') and check_twitter_post(link):
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


def checkpost(url:str) -> bool:

    '''
        This function checkpost() returns True or False if the post is valid or invalid respectively.
    '''

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the article titles by inspecting the HTML structure
        articles = soup.find_all("h2", class_="article-title")

        # Iterate through the list of articles and print their titles
        for article in articles:
            print(article.text)
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)

