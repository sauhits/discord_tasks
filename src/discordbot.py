from discord.ext import commands
import discord,dotenv,os
import databaseController
import get,format


dotenv.load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


@bot.event
async def onready():
    print("Bot is ready")

@bot.command()
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


bot.run(TOKEN)