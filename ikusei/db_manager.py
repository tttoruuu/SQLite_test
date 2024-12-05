import sqlite3
import bcrypt

# データベースの初期化
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ユーザーテーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        experience INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
    """)

    # ToDoテーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_name TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()

# ユーザー登録
def register_user(nickname, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (nickname, password_hash) VALUES (?, ?)", (nickname, password_hash))
        conn.commit()
        print(f"ユーザー {nickname} が登録されました！")
    except sqlite3.IntegrityError:
        print("そのニックネームは既に登録されています。")
    finally:
        conn.close()

# ユーザー認証
def login_user(nickname, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, password_hash FROM users WHERE nickname = ?", (nickname,))
    user = cursor.fetchone()

    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[1]):
        return user[0]  # ユーザーIDを返す
    return None

# タスク追加
def add_task(user_id, task_name):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO todos (user_id, task_name, status) VALUES (?, ?, ?)", (user_id, task_name, "未完了"))
    conn.commit()
    conn.close()

# タスク取得
def get_tasks(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, task_name, status FROM todos WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# タスクステータス更新と経験値加算
def update_task_status(task_id, new_status, user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # タスクのステータスを更新
    cursor.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()

    # タスク完了時に経験値を追加
    if new_status == "完了":
        add_experience(user_id, xp_to_add=10)

    conn.close()

# 経験値の追加とレベルアップ
def add_experience(user_id, xp_to_add=10):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ユーザーの現在の経験値とレベルを取得
    cursor.execute("SELECT experience, level FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user is None:
        return

    current_xp, current_level = user
    new_xp = current_xp + xp_to_add

    # レベルアップの閾値
    xp_threshold = 100
    if new_xp >= xp_threshold:
        new_level = current_level + 1
        new_xp -= xp_threshold
        print(f"レベルアップしました！新しいレベル: {new_level}")
    else:
        new_level = current_level

    # データベースを更新
    cursor.execute("UPDATE users SET experience = ?, level = ? WHERE id = ?", (new_xp, new_level, user_id))
    conn.commit()
    conn.close()

# ユーザー情報取得
def get_user_info(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT experience, level FROM users WHERE id = ?", (user_id,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info
