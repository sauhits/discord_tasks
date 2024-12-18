from discord.ext import commands
import discord
import databaseController
import dotenv
import os


dotenv.load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


@bot.event
async def onready():
    print("Bot is ready")

@bot.command()
async def kadai(ctx):
    table=databaseController.showTasks()
    await ctx.send(table)

@bot.command()
async def add(ctx, title: str, deadline: str):
    databaseController.insertTask(str(title), str(deadline))
    await ctx.send("タスクを追加しました。")

# 退出
@bot.command()
async def exit(ctx):
    await ctx.send("Goodbye!")
    await bot.close()


@bot.command()
async def delete(ctx, id):
    if databaseController.deleteTask(str(id)):
        await ctx.send(f"タスクID{id}を削除しました。")
    else:
        await ctx.send(f"タスクID{id}は存在しません。")


bot.run(TOKEN)
