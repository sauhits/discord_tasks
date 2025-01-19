from discord.ext import commands
from dotenv import load_dotenv
import discord, os
import get, format, teams_get, teams_format
import datetime

load_dotenv()

SSO_USERNAME = os.environ.get("SSO_USERNAME")
SSO_PASSWORD = os.environ.get("SSO_PASSWORD")
OTP_SEC_KEY = os.environ.get("OTP_SEC_KEY")
URL = os.environ.get("GAKUJO_URL")
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("login ")
    try:
        await tree.sync()
        print("synced")
    except Exception as e:
        print("failed to sync")
        print(e)


@tree.command(name="tasks_view", description="課題一覧を表示します")
async def tasks_view(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    log_space = "log_kadai"
    threads = discord.utils.get(interaction.guild.threads, name=log_space)
    if threads is None:
        await interaction.followup.send(f"{log_space}が見つかりません")
        return
    async for message in threads.history(limit=20):
        if message.author.name == "kadai":
            send_time = message.created_at
            time_now_utc = datetime.datetime.now(datetime.timezone.utc)
            # logの期限を確認
            if (time_now_utc - send_time).seconds < 86400:
                await interaction.followup.send(message.content)
                return
    # タスクを取得して整形
    getTaskList = get.getTaskList(URL, SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY)
    task_text = [task.text for task in getTaskList]
    task_table = format.taskFormatter(task_text)
    # Markdown形式でテーブルを作成
    table = "```\n"  # コードブロックで囲んで、テーブル形式に見せる
    for row in task_table:
        table += (
            " | ".join([str(cell) for cell in row]) + "\n"
        )  # 行を「 | 」で区切り、各セルを文字列として処理
    table += "```"
    # 表を送信
    await threads.send(table)
    await interaction.followup.send(table)


@tree.command(name="teams_view", description="Teamsの課題一覧を表示します")
async def teams_view(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    getTaskList = teams_get.getTeamsTasks(SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY)
    task_list = teams_format.taskFormatter(getTaskList)
    print(task_list)
    for task in task_list:
        await interaction.followup.send(task)


client.run(TOKEN)
