import streamlit as st
from db_manager import init_db, register_user, login_user, add_task, get_tasks, update_task_status, get_user_info

# データベース初期化
init_db()

# セッション管理
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("ToDo進捗管理アプリ with レベルアップ")

# ログインまたは新規登録
if st.session_state.user_id is None:
    st.sidebar.subheader("ログインまたは新規登録")

    # 新規登録
    if st.sidebar.checkbox("新規登録"):
        nickname = st.sidebar.text_input("ニックネーム")
        password = st.sidebar.text_input("パスワード", type="password")
        if st.sidebar.button("登録"):
            register_user(nickname, password)
            st.sidebar.success("登録が完了しました！")

    # ログイン
    nickname = st.sidebar.text_input("ログイン: ニックネーム")
    password = st.sidebar.text_input("ログイン: パスワード", type="password")
    if st.sidebar.button("ログイン"):
        user_id = login_user(nickname, password)
        if user_id:
            st.session_state.user_id = user_id
            st.sidebar.success(f"{nickname} としてログインしました！")
        else:
            st.sidebar.error("ニックネームまたはパスワードが間違っています。")
else:
    st.sidebar.write("ログイン中")
    if st.sidebar.button("ログアウト"):
        st.session_state.user_id = None

# タスク管理
if st.session_state.user_id:
    user_info = get_user_info(st.session_state.user_id)
    if user_info:
        experience, level = user_info
        st.sidebar.write(f"レベル: {level}")
        st.sidebar.write(f"経験値: {experience} / 100")

    st.subheader("タスク一覧")
    tasks = get_tasks(st.session_state.user_id)
    for task in tasks:
        task_id, task_name, status = task
        st.write(f"ID: {task_id}, タスク: {task_name}, ステータス: {status}")
        if status == "未完了" and st.button(f"完了: {task_id}"):
            update_task_status(task_id, "完了", st.session_state.user_id)
            st.rerun()

    # 新しいタスクの追加
    task_name = st.text_input("新しいタスク")
    if st.button("タスクを追加"):
        add_task(st.session_state.user_id, task_name)
        st.rerun()
