from discord.ext import commands
import discord
import random
import databaseController

TOKEN = "MTMxNDEzMTg5Nzk5MDkwNTkzOA.Gj61gh.uIiGfouXCZBIFmPRd9Spl140mXV91c1af13Q_o"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

cor = databaseController.dbConnect()


@bot.event
async def onready():
    if cor != None:
        print("Connected to database\n")
    print("Bot is ready")


@bot.command()
async def kadai(ctx):
    try:
        table = databaseController.showTasks(cor)
        print(table)
        await ctx.send(table)
    except Exception as e:
        print(e)
        await ctx.send("エラーが発生しました。")


# 退出
@bot.command()
async def exit(ctx):
    await databaseController.dbClose(cor)
    if cor == None:
        print("データベース接続を閉じました。")
    await ctx.send("Goodbye!")
    await bot.close()


bot.run(TOKEN)
