from agents import Agent, Runner
from db.messages import get_messages, add_message

MODEL_NAME = "gpt-4o-mini"

teacher_php = Agent(
    model="gpt-4o-mini",
    name="PHP 講師",
    instructions="你是一位專門教授 PHP 的講師，講話方式很可愛",
    handoff_description="專門講授 PHP 程式語言",
)

teacher_f2e = Agent(
    model="gpt-4.1-nano",
    name="前端講師 - 酷落",
    instructions="你是一位熟悉 Vue 的前端講師，有一本暢銷書「重新認識Vue.js」",
    handoff_description="專門講授 Vue.js 並推廣技術社群",
)

teacher_python = Agent(
    model="gpt-4o-mini",
    name="Python 講師 - 菜市場阿龍",
    instructions="""
      - 你是一位專門教授 Python 的講師，而且還寫了一本「為你自己學 Python」的書
      - 個性不好相處，口頭禪是「啊我就..」
    """,
    tools=[],
    handoff_description="講授 Python 程式語言以及相關的套件",
)

agent = Agent(
    model="gpt-4.1",
    name="五倍學院班導師",
    instructions="你是一位細心、照顧學生的班導師，專門照顧學員們的生活起居以及大小雜事",
    handoffs=[teacher_php, teacher_f2e, teacher_python],
)

print("緩光臨~五倍學院，請問你想學點什麼嗎？")

try:
    while True:
        user_input = input("→ ").strip()

        if user_input.lower() == "exit":
            print("寫光您!")
            break

        add_message(user_input)
        result = Runner.run_sync(agent, get_messages())
        content = result.final_output
        add_message(content, role="assistant")

        print(content)

except (EOFError, KeyboardInterrupt):
    print("寫光您!")
