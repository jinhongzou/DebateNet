
import os
from pydantic_ai.common_tools.tavily import tavily_search_tool

from code.utils.dspy_models import Classifier
from code.utils.config4prompt import debate_prompt_json
from code.utils.debate import Debate

from dotenv import load_dotenv

# 加载环境变量文件（如果存在）
load_dotenv()

# 从环境变量中获取API密钥，如果没有设置则使用默认值（可选）
tavily_api_key = os.getenv('TAVILY_API_KEY', 'your-default-key-if-any')
siliconflow_api_key = os.getenv('SILICONFLOW_API_KEY', 'your-default-key-if-any')

# 如果没有设置环境变量，可以提示用户或抛出异常
if not siliconflow_api_key:
    raise ValueError("API keys not found. Please set SILICONFLOW_API_KEY environment variables.")


if __name__ == "__main__":

    current_script_path = os.path.abspath(__file__)
    MAD_path = current_script_path.rsplit("/", 1)[0]

    classifyagent = Classifier(#model='openai/Qwen/Qwen2.5-32B-Instruct', 
                               model='openai/Qwen/Qwen2.5-7B-Instruct',
                               api_key=siliconflow_api_key, 
                               api_base='https://api.siliconflow.cn/v1')

    config =  debate_prompt_json()
    debate = Debate(max_round=3,
                    model_name="Qwen/Qwen2.5-7B-Instruct",
                    openai_api_key=siliconflow_api_key, 
                    #tools=[tavily_search_tool(tavily_api_key)],
                    config=config, 
                    temperature=0, 
                    sleep_time=0)

    chat_model=''

    while True:

        while chat_model not in {"1", "2", "3"}:
            chat_model = input("\nEnter the chat_model [1:auto; 2:chat; 3:debate]: ").strip()

        debate_topic = ""
        while debate_topic == "":
            debate_topic = input(f"\nEnter your debate topic: ")

        if chat_model == "1": # 自动判断模式

            classify=classifyagent.classify_question(debate_topic)

            if classify.Category == 'Answer':
                response = classify.Answer
                print(f"This is a direct answer question. The answer is:\n{response}")

            else :# 辩论模式
                print(f"This is a debate question. Let's start the debate on the topic ...\n")
                #debate.run()
                debate.run_loop(debate_topic)
                response= debate.get_answer()
                print(f"\nThis is the debate result: {response}")

        elif chat_model == "2": # 单一模型
            classify=classifyagent.classify_question(debate_topic)

            if classify.Category == 'Answer':
                response = classify.Answer
                print(f"This is a direct answer question. The answer is:\n{response}")

        elif chat_model == "3": # 辩论模式
            print(f"This is a debate question. Let's start the debate on the topic ...\n")
            #debate.run()
            debate.run_loop(debate_topic)
            response= debate.get_answer()
            print(f"\nThis is the debate result: {response}")
