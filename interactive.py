"""
MAD: Multi-Agent Debate with Large Language Models
Copyright (C) 2023  The MAD Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
if not tavily_api_key or not siliconflow_api_key:
    raise ValueError("API keys not found. Please set TAVILY_API_KEY and SILICONFLOW_API_KEY environment variables.")
'''
def tavily_search_tool(api_key: str):
    """Creates a Tavily search tool.

    Args:
        api_key: The Tavily API key.

            You can get one by signing up at [https://app.tavily.com/home](https://app.tavily.com/home).
    """
    return Tool(
        TavilySearchTool(client=AsyncTavilyClient(api_key)).__call__,
        name='tavily_search',
        description='Searches Tavily for the given query and returns the results.',
    )
'''

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
