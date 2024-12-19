import re


# リストで渡した課題データを[[title,deadline]]の形式に変換する
def taskFormatter(raw_text):
    # ヘッダーの削除
    raw_text.pop(0)
    task_formatted = []
    for task in raw_text:
        # 半角，全角，タブを削除
        task = re.sub(r"[\u3000 \t]", "", task)

        # タイトルの取得をする．
        title = re.search(r"^\S+\d+クラス", task)
        if title:
            title = title.group()
            title = re.sub(
                r"^(小テスト|レポート|授業アンケート|学内アンケート|授業評価アンケート)|\(\d+クラス$",
                "",
                title,
            )
        else:
            print("タイトルが取得できませんでした")
            continue

        # 締切の取得をする
        deadline = re.search(r"～\d{4}/\d{2}/\d{4}:\d{2}", task)
        if deadline:
            deadline = deadline.group()
            deadDate = int(re.sub(r"～|/|\d{2}:\d{2}", "", deadline))
        else:
            print("締切が取得できませんでした")
            continue

        # 締切時間によって日時を変更する
        deadTime = int(re.sub(r"～\d{4}/\d{2}/\d{2}|:", "", deadline))
        if deadTime < 2300:
            deadDate = deadDate - 1

        task_formatted.append((title, deadDate))
    return task_formatted
