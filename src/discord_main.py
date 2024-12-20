from discord.ext import commands
from dotenv import load_dotenv
import discord,os
import databaseController
import get,format


load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def kadai(ctx):
    # タスクを取得して整形
    getTaskList = get.getTaskList()
    task_text = [task.text for task in getTaskList]
    task_table = format.taskFormatter(task_text)

    # Markdown形式でテーブルを作成
    table = "```\n"  # コードブロックで囲んで、テーブル形式に見せる
    for row in task_table:
        table += " | ".join([str(cell) for cell in row]) + "\n"  # 行を「 | 」で区切り、各セルを文字列として処理
    table += "```"

    # 表を送信
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
