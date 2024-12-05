import sqlite3

def update_user_table():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # `experience` カラムを追加（存在しない場合のみ）
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN experience INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        print("`experience` カラムは既に存在します。")

    # `level` カラムを追加（存在しない場合のみ）
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        print("`level` カラムは既に存在します。")

    conn.commit()
    conn.close()

update_user_table()