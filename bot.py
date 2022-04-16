import discord
import requests
import os
from discord.ext import tasks
import asyncio
import datetime as dt
import random
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
#get the token
TOKEN = os.getenv('DISCORD_TOKEN')

global paimordle_index 
paimordle_index = 74
global wordsWeek
wordsWeek = []

#connect to the discord client
client = discord.Client()

#for command functions use the bot
bot = commands.Bot(command_prefix = 'pai ')

#on ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')
    for guild in bot.guilds:
        print(guild.text_channels[1])

#get the bot ready with a bot event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'paimon' in message.content:
        response = "Hi! i'm Pymon!"
        await message.channel.send(response)
    await bot.process_commands(message)

@bot.command(name = "aboutme")
async def info(ctx):
    inf = "this bot is the first bot I have ever developed, in the hopes of learning how to use APIs, especially with python. \n"
    inf+=("the APIs at work here are Discord, and paimon.moe !\nyou can use the command help to have the list of commands. ")
    await ctx.channel.send(inf)

@bot.command(name = "banner")
async def banner(ctx, type):
    if(type == "character"):
        response = requests.get("https://github.com/MadeBaruna/paimon-moe-api/blob/main/src/routes/wish.ts")
        if response.status_code == 200:
            print(response.content)

@bot.command(name="commands", description="Returns all commands available")
async def helps(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

def getWord(todayIndex):
    response = requests.get("https://paimordle.vercel.app/static/js/main.8df5c693.js")
    print(response.status_code)
    fullCode = response.content.decode("utf-8")
    startindex = fullCode.index("s=[\"")
    endindex = fullCode.index("],c=")
    solutionWords = fullCode[startindex+3:endindex]
    solutionWords = solutionWords.replace("\"", "")
    words = solutionWords.split(",")
    return (words[todayIndex-1:todayIndex+7])

@tasks.loop(hours = 24.0)
async def paimordle():
    global paimordle_index
    paimordle_index += 1
    global wordsWeek
    wordsWeek = getWord(paimordle_index)

@bot.command(name = 'paimordle')
async def paimordleGet(message, which):
    allWeek = ""
    if(which == "today"):
        await message.channel.send(f"today's paimordle is: \n{wordsWeek[1]}")
    if(which == "week"):
        i=1
        while i < len(wordsWeek):
            allWeek+= (wordsWeek[i]+ "\n")
            i+=1
        await message.channel.send(f"this weeks's paimordles are: \n{allWeek}")
    if(which == "yesterday"):
        await message.channel.send(f"yesterday's paimordle is: \n{wordsWeek[0]}")


####################################################################################################################################################
#for the reminders and role pings, i create a repo on github, where all the server ids are saved
#create a command that activates reminders, and role pings
#command demands what kind of reminders should be added, ads the roles and the channel
#creates channel if not existant (search with channel name)
#saves the information in the repo
#saves in the server id list if each id has what ping activated, every 5 minute, bot updates the roles they should ping
#the update should be done inside the on ready event
#so every 5 minute the bot gets the list of guilds with the ping activated
#if the ping is on and the channel doesn't exist or the roles don't exist, it will create it 
#after that it has another scheduler that calls the checkinreminder function to ping the role at 5 pm every day
#when the checkin scheduler hits 5 pm it will call the checkin function
#the function will loop through all the servers in the database, get the server, channel and role ids and ping the according role
#will see if we can pass the database list through the function from on_ready or create a request within the checkin function
#add role assigning command to give the ping roles to whoever wants it
#####################################################################################################################################################
async def checkInReminder():
    pass
#####################################################################################################################################################
#for the database, we will be using a private repo as a rest api
#that repo will have a few json files, one for the list of servers that the bot is in and their informations
    #for the servers, the info will be: the id as main identifier
        #name of the server
        #checkin reminder activated (boolean)
        #banner change ping (boolean)
        #think about future pings i guess
        #
    #for the profiles, the info will be: the account discord id as identifier
        #main UID
        #list of secondary account UIDs
        #retrieves server region from main UID
        #main character
        #
    #reports database: auto genned ID of the report (token)
        #the date and time that it was sent
        #the object
        #the tags
        #the content (issue or recommendations)
        #discord id of the person that sent it
        #state (bool, resolved or not)
#when the bot checks for servers every 5 minutes, it will also check if a new server has been added, or deleted, and updates the json file accordingly
#####################################################################################################################################################
#run the bot
paimordle.start()
bot.run(TOKEN)
