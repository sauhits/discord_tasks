import re

test = [
    "Jan 21st\nTomorrow\nグループ自由課題・企画構想\nDue at 11:59 PM\n2024応用プログラミングC\nレポート課題rp5必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\n当日課題ex6必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nNext week\nJan 28th\nTuesday\nレポート課題rp6必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nFurther out\nFeb 4th\nTuesday\nレポート課題rp01発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp02発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp03発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex01発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex02発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex03発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp04発展課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nレポート課題rp5発展課題 (提出は任意)\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nレポート課題rp6発展課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points"
]

# 渡した課題データを [(title, deadline)] の形式に変換する
def taskFormatter(raw_text):
    task_list = []
    deadline = ""
    deadtime = ""
    title = ""

    # 正規表現の修正
    re_point = re.compile(r"^\d+\s?points$")
    re_deadline = re.compile(r"^[A-Za-z]{3}\s\d{1,2}(st|nd|rd|th)?$")
    re_deadtime = re.compile(r"^Due at \d{1,2}:\d{2} (AM|PM)$")
    re_weekday = re.compile(r"^(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)$")
    re_weekspan = re.compile(r"^(Tomorrow|Next week|Further out)$")

    # テキストを改行で分割
    raw_text_list = raw_text[0].split("\n")
    
    for target in raw_text_list:
        # 改行と空白を削除する
        target = target.strip()
        if not target:
            continue

        # deadlineの取得
        if re_deadline.match(target):
            deadline = deadLineFormatter(target)
            continue

        # deadtimeの取得
        if re_deadtime.match(target):
            deadtime = deadTimeFormatter(target)
            # タスク情報を追加
            task_list.append((title, f"{deadline} {deadtime}"))
            continue

        # points, 曜日, span のスキップ処理
        if re_point.match(target) or re_weekday.match(target) or re_weekspan.match(target):
            continue

        # title の更新
        title = target

    return task_list

def deadTimeFormatter(deadtime: str):
    # "Due at " を削除
    deadtime = re.sub(r"^Due at ", "", deadtime)
    hour, minute = map(int, deadtime[:-3].split(":"))
    period = deadtime[-2:]
    if period == "PM" and hour != 12:
        hour += 12
    elif period == "AM" and hour == 12:
        hour = 0
    return f"{hour:02}{minute:02}"

def deadLineFormatter(deadline: str):
    # 月名を数値に変換
    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    deadline = re.sub(r"(st|nd|rd|th)$", "", deadline)
    month, day = deadline.split()
    return f"{month_map[month]}{int(day):02}"

# 結果を確認
formatted_tasks = taskFormatter(test)
print(formatted_tasks)
