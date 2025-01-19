import re


test = [
    "Jan 21st\nTomorrow\nグループ自由課題・企画構想\nDue at 11:59 PM\n2024応用プログラミングC\nレポート課題rp5必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\n当日課題ex6必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nNext week\nJan 28th\nTuesday\nレポート課題rp6必須課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nFurther out\nFeb 4th\nTuesday\nレポート課題rp01発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp02発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp03発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex01発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex02発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\n当日課題ex03発展課題 (提出は任意)\nDue at 12:01 AM\n2024応用プログラミングC\n30 points\nレポート課題rp04発展課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nレポート課題rp5発展課題 (提出は任意)\nDue at 11:59 PM\n2024応用プログラミングC\n100 points\nレポート課題rp6発展課題\nDue at 11:59 PM\n2024応用プログラミングC\n100 points"
]


# 渡した課題データを[(title,deadline)]の形式に変換する
def taskFormatter(raw_text):
    task_list = []
    i: int = 0
    deadline: str = ""
    deadtime: str = ""
    title: str = ""
    skip: bool = False
    re_point = re.compile(r"^\d+points$")
    re_deadline = re.compile(r"^\w{3}\d+\w{2}$")
    re_deadtime = re.compile(r"^Dueat\d{2}:\d{2}\w{2}$")
    re_weekday = re.compile(
        r"^(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)+$"
    )
    re_weekspan = re.compile(r"^[A-Za-z\s]+$")
    # リストに整形
    raw_text_list = raw_text[0].split("\n")
    for target in raw_text_list:
        if skip:
            skip = False
            continue
        # 改行と空白を削除する
        target = re.sub(r"[\u3000 \t]", "", target)
        # deadlineの取得
        if re_deadline.match(target):
            deadline = deadLineFormatter(target)
            continue
        # 締切の取得
        if re_deadtime.match(target):
            deadtime = deadTimeFormatter(target)
            # listに追加
            task_list.append((title, deadline + " " + deadtime))
            skip = True
            continue
        # point行,曜日行,span_nameのcontinue
        if (
            re_point.match(target)
            or re_weekday.match(target)
            or re_weekspan.match(target)
        ):
            continue
        title = target
    return task_list


def deadTimeFormatter(deadtime: str):
    deadtime = re.sub(r"^Dueat", "", deadtime)
    formatted_deadtime = ""
    if re.sub(r"^\d{2}:\d{2}", "", deadtime) == "PM":
        tmp = int(re.sub(r":", "", re.sub(r"[a-zA-Z]{2}$", "", deadtime))) + 1200
        formatted_deadtime = str(tmp)[0:2] + ":" + str(tmp)[2:4]
    else:
        formatted_deadtime = re.sub(r"[a-zA-Z]{2}$", "", deadtime)
    return formatted_deadtime


def deadLineFormatter(deadline: str):
    month_map = {
        "Jan": "1",
        "Feb": "2",
        "Mar": "3",
        "Apr": "4",
        "May": "5",
        "Jun": "6",
        "Jul": "7",
        "Aug": "8",
        "Sep": "9",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    month = month_map.get(re.match(r"^\w{3}", re.sub(r"\w{2}$", "", deadline)).group())
    day = re.sub(r"^\w{3}", "", re.sub(r"\w{2}$", "", deadline))
    return month + "/" + day


print(taskFormatter(test))
