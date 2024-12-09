from discord.ext import commands
import discord
import databaseController
import dotenv
import os


dotenv.load_dotenv()
TOKEN = os.environ.get("Discord_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


@bot.event
async def onready():
    print("Bot is ready")
    


@bot.command()
async def kadai(ctx):
    table=databaseController.showTasks(ctx)
    await ctx.send(table)


# 退出
@bot.command()
async def exit(ctx):
    await ctx.send("Goodbye!")
    await bot.close()


bot.run(TOKEN)