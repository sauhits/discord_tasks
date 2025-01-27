from discord.ext import commands
from dotenv import load_dotenv
import discord, os, copy
import gakujo_get, gakujo_format, teams_get, teams_format,sort
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


def dateToInt(date: datetime) -> int:
    year = str(date.year)
    if date.month < 10:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
    if date.hour < 10:
        hour = "0" + str(date.hour)
    else:
        hour = str(date.hour)
    return int(year + month + day + hour)


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
            send_time = dateToInt(message.created_at)
            time_now_utc = dateToInt(datetime.datetime.now(datetime.timezone.utc))
            # logの期限を確認
            if (time_now_utc - send_time) < 24:
                await interaction.followup.send(message.content)
                return

    # タスクを取得して整形
    getGakujoTasks = gakujo_get.getTaskList(
        URL, SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY
    )
    gakujo_tasks = copy.deepcopy(gakujo_format.taskFormatter(getGakujoTasks))
    gakujo_get.close()
    await interaction.followup.send("学情の課題を取得しました")
    getTeamsTasks = teams_get.getTeamsTasks(SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY)
    teams_tasks = copy.deepcopy(teams_format.taskFormatter(getTeamsTasks))
    teams_get.close()
    await interaction.followup.send("Teamsの課題を取得しました")
    task_all = gakujo_tasks + teams_tasks
    print(task_all)
    task_all = sort.sort(task_all)
    print(task_all)
    # Markdown形式でテーブルを作成
    table = "```\n"  # コードブロックで囲んで、テーブル形式に見せる
    table += "| 期限      | 課題名       \n"  # ヘッダー行
    table += "|----------|--------------\n"  # ヘッダーの区切り線
    for row in task_all:
        task_parts = row.split('.')
        table += f"| {task_parts[0]} | {task_parts[1]} \n"  # 「.」で分割してテーブルの行を作成
    table += "```"
    # 表を送信
    await threads.send(table)
    await interaction.followup.send(table)


client.run(TOKEN,reconnect=True)
