import streamlit as st
from openai import OpenAI

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
client = OpenAI(
    api_key=st.secrets["OpenAIAPI"]["openai_api_key"]
)

system_prompt = """
あなたは熱狂的な地球平面説信者です。
どんな話題を振られても地球平面説の話題に自然にシフトします。
地球平面説を信じない人にはだんだんと対応が冷たくなります。

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": system_prompt
        }
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

    for message in reversed(messages[1:]):
        speaker = "🙂"

        if message["role"] == "assistant":
            speaker = "🤖"

        st.write(speaker + ": " + message["content"])
