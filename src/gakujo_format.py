import re

test = [
    "提出物種別\n講義名\n学期/曜日・時限\nタイトル\n状態\n提出期間\n提出状況",
    "レポート 人工知能概論(1クラス)\n後期後半/火1・2, 後期前半/火1・2 人工知能概論：後半レポート課題 受付中 2025/01/14 00:00 ～ 2025/02/04 23:55 未提出",
    "レポート コンパイラ(1クラス)\n後期前半/水7・8, 後期後半/水7・8 最終試験レポート 受付中 2025/01/15 08:00 ～ 2025/01/30 00:00 提出済",
    "レポート スポーツⅡ(情)\n後期前半/金3・4, 後期後半/金3・4 スポーツIIレポート課題 受付中 2025/01/22 00:00 ～ 2025/01/31 17:00 未提出",
    "小テスト 数理論理Ⅱ(1クラス)\n後期後半/金9・10 第2回 web小テスト 受付中 2025/01/21 17:30 ～ 2025/01/30 23:55 提出済",
    "レポート ディジタル信号処理(1クラス)\n後期前半/月5・6, 後期後半/月5・6 最終レポート 受付中 2025/01/26 16:30 ～ 2025/02/09 23:55 未提出",
]


# リストで渡した課題データを[(title, deadline)]の形式に変換する
def taskFormatter(raw_text: list):
    raw_text = [task.text for task in raw_text]
    # ヘッダーを削除
    raw_text.pop(0)
    task_formatted = []

    for task in raw_text:
        # 半角，全角，タブを削除
        task = re.sub(r"[\u3000 \t]", "", task)

        # タイトルの取得
        title_match = re.match(r"^[^\n]+", task)
        if title_match:
            title = title_match.group()
            # 不要部分を削除
            title = re.sub(
                r"^(小テスト|レポート|授業アンケート|学内アンケート|授業評価アンケート)\s*",
                "",
                title,
            )
            title = re.sub(r"\(.*\)$", "", title)
        else:
            print("タイトルが取得できませんでした")
            continue

        # 締切の取得
        deadline_match = re.search(r"～(\d{4}/\d{2}/\d{2})(\d{2}:\d{2})", task)
        if deadline_match:
            date_str, time_str = deadline_match.groups()
            month_day = date_str[5:].replace("/", "")
            time_str = time_str.replace(":", "")
            deadline_time = int(time_str)

            # 時刻が23時未満の場合、締切日を前日に変更
            if deadline_time < 2300:
                day = int(month_day[2:]) - 1
                month_day = month_day[:2] + f"{day:02}"
        else:
            print("締切が取得できませんでした")
            continue

        # 結果をリストに追加
        task_formatted.append((f"{month_day}{time_str}", title))

    return task_formatted


# formatted_tasks = taskFormatter(test)
# print(formatted_tasks)
