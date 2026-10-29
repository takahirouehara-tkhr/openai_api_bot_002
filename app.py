
import streamlit as st
from openai import OpenAI

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {
        "role": "user",
        "content": st.session_state["user_input"]
    }

    messages.append(user_message)

    response = client.chat.completions.create(
        model="gpt-6-luna",
        messages=messages
    )

    # ChatCompletionMessageオブジェクトを辞書に変換して保存
    bot_message = {
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content
    }

    messages.append(bot_message)

    st.session_state["user_input"] = ""


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input(
    "メッセージを入力してください。",
    key="user_input",
    on_change=communicate
)


if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
