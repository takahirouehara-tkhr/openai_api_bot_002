import streamlit as st
from openai import OpenAI

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
client = OpenAI(
    api_key=st.secrets["OpenAIAPI"]["openai_api_key"]
)

system_prompt = """
あなたは優秀な料理研究家です。
限られた食材や時間で、様々な料理のレシピを提案することができます。
あなたの役割はレシピを考えることなので、例えば以下のような料理以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
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
st.title(" 「レシピ」を考えるチャットボット")
st.write("どんな食事を作りたいですか？")

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
