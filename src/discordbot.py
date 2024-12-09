from discord.ext import commands
import discord
import random
import databaseController

TOKEN = "MTMxNDEzMTg5Nzk5MDkwNTkzOA.Gj61gh.uIiGfouXCZBIFmPRd9Spl140mXV91c1af13Q_o"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


@bot.event
async def onready():
    print("Bot is ready")


@bot.command()
async def kadai(ctx):
    await ctx.send("Hello World!")


bot.run(TOKEN)
