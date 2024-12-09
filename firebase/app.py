import streamlit as st
from firebase_admin import credentials, initialize_app, auth
import json

# Firebaseの初期化
def initialize_firebase():
    # StreamlitのSecretsからFirebaseサービスアカウントキーを取得
    firebase_secrets = json.loads(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_secrets)
    initialize_app(cred)

# ユーザー登録
def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success(f"新しいユーザーが作成されました: {user.uid}")
        return user
    except Exception as e:
        st.error(f"ユーザー登録中にエラーが発生しました: {e}")

# ログイン（認証用トークン生成）
def login_user(email, password):
    try:
        # Firebase Authenticationはサーバーサイドでパスワードを確認するAPIがないため、フロント側でFirebase SDKを利用
        st.warning("ログインはクライアントサイドのFirebase SDKが必要です（例：JavaScriptで実装）")
    except Exception as e:
        st.error(f"ログイン中にエラーが発生しました: {e}")

# Streamlit UI
def app():
    st.title("Firebase Authentication Example")

    # Firebaseの初期化
    if "firebase_initialized" not in st.session_state:
        initialize_firebase()
        st.session_state["firebase_initialized"] = True

    # タブで登録とログインを切り替える
    mode = st.radio("選択してください", ["ログイン", "新規登録"])

    if mode == "新規登録":
        st.subheader("新規登録")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        if st.button("登録"):
            register_user(email, password)

    elif mode == "ログイン":
        st.subheader("ログイン")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        if st.button("ログイン"):
            login_user(email, password)

# アプリの起動
if __name__ == "__main__":
    app()
