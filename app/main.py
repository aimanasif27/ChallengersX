import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

from checkpost import check_linkedin_post, check_twitter_post
from mongo import insert_details, register_user, fetch_user_participation_and_create_pdf


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
        await ctx.send("Please enter the details in valid format i.e. `!cx register #xevent x@example.com Full Name`")
    else:
        print(args)
        discord_id = ctx.author.name

        if len(args) == 4:
            event, email, fname, lname = args
            name = fname+' '+lname
            register_user(event, email, name, discord_id)
            await ctx.send(f"{name}, You are successfully registered for {event}!")
        elif len(args) == 3:
            event, email, name = args
            register_user(event, email, name, discord_id)
            await ctx.send(f"{name}, You are successfully registered for {event}!")
        else:
            await ctx.send(f'Please enter the details in valid format i.e. `!cx register #xevent x@example.com Full Name`')
               
    
# Command: ndaysofcode
@bot.command()
async def _365Daysofcode(ctx, *args):
    event = '#365DaysofCode'
    if not args:
        await ctx.send("You didn't provide a link.")
    else:
        link : str = ' '.join(args)
        print("TypeofLink: ", type(link))
        if link.startswith('https://www.linkedin.com') and check_linkedin_post(link, event):
          
            if insert_details(ctx.author.name, event, link):
                await ctx.send("We noted your response!")
            else: 
                await ctx.send(f"{ctx.author}, You didn't registered for {event}")
        elif (link.startswith('https://twitter.com') or link.startswith('https://x.com')) and check_twitter_post(link, event):
            if insert_details(ctx.author.name, event, link):
                await ctx.send("We noted your response!")
            else:
                await ctx.send(f"{ctx.author}, You didn't registered for {event}")
        else:
            await ctx.send("You didn't provide correct LinkedIn or Twitter post link!")

# Command: Result
@bot.command()
async def result(ctx, *args):
    admin_roles = ['Admin', 'Team-Scaler']
    if any(role.name in admin_roles for role in ctx.author.roles):
        if not args:
            await ctx.send("Please provide valid event!")
        elif args[0].startswith('#') and len(args) == 1:
            print('Generating result ...')
            
            event_hashtag = args[0]

            file_name = fetch_user_participation_and_create_pdf(event_hashtag)
            
            # Open the PDF file
            with open(file_name, 'rb') as file:
                pdf_file = discord.File(file, filename='user_participation_details.pdf')

            # Send the PDF file as a reply to the same channel
            await ctx.send(file=pdf_file)
    
            await ctx.send(f"PDF file '{file_name}'created successfully!")
        else:
            await ctx.send("Please provide valid event!")
    else:
        await ctx.send("You do not have permission to use this command.")


# Command: Help
@bot.command()
async def _help(ctx):
    await ctx.send('''
                   Below are some commands:
                   - Use `!cx #365Daysofcode <link>` to post your submission,
                   - Use `!cx register <event_hashtag> <emailexample.com> <Full Name>` to Register for the event,
                   - Use `!cx result <event_hashtag>` to get the result, this command is only accessed by `Admin`.
                   ''')

# Error handler for CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!cx _help` to see available commands.")


bot.run(TOKEN)
