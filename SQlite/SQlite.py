import streamlit as st
import sqlite3

# データベース操作関数
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_task(task_name):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, status) VALUES (?, ?)", (task_name, "未完了"))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Streamlit UI
init_db()

st.title("タスク管理アプリ")

# タスク追加
task_name = st.text_input("タスク名を入力:")
if st.button("タスクを追加"):
    add_task(task_name)
    st.success(f"タスク '{task_name}' を追加しました！")

# タスク一覧表示
tasks = get_tasks()
st.write("### タスク一覧")
for task in tasks:
    st.write(f"ID: {task[0]} - タスク: {task[1]} - ステータス: {task[2]}")
