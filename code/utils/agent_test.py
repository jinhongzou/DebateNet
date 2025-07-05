
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from typing import Optional
from pydantic_ai import Agent

from code.utils.pydantic_agent import PydanticAgent, Classifier, DebateJudgment

# 示例用法
if __name__ == "__main__33":

    model = OpenAIModel(
        #'Qwen/Qwen3-8B'
        model_name='Qwen/Qwen2.5-7B-Instruct',
        provider=OpenAIProvider(
            base_url='https://api.siliconflow.cn/v1',
            api_key=''
        ),
    )

    play_agent = Agent(model=model, name='', output_type=str,
                       system_prompt='',
                        model_settings={'tool_choice': 'auto'})

    play = PydanticAgent(play_agent,'test_agent')


    while True:
        debate_topic = ""
        while debate_topic == "":
            debate_topic = input(f"\nEnter your debate topic: ")
        resutl=play.ask(debate_topic)
        print(resutl)

    # D:\github_rep\Multi-Agents-Debate\code\utils> python .\agent_test.py

# 示例用法 Classifier
if __name__ == "__main__22":

    classifyagent = Classifier(#model='openai/Qwen/Qwen3-8B', 
                               model='openai/Qwen/Qwen2.5-7B-Instruct',
                               api_key='sk-xxx', 
                               api_base='https://api.siliconflow.cn/v1')


    while True:
        debate_topic = ""
        while debate_topic == "":
            debate_topic = input(f"\nEnter your debate topic: ")
        resutl=classifyagent.classify_question(debate_topic)
        print(resutl)

# 示例用法 DebateJudgment
if __name__ == "__main__":

    debatejudgment = DebateJudgment(model='openai/Qwen/Qwen2.5-7B-Instruct', 
                                    #model='openai/Qwen/Qwen2.5-32B-Instruct',
                                    api_key='sk-xxx', 
                                    api_base='https://api.siliconflow.cn/v1')

    debate_topic = '''
Affirmative side arguing:
要解决这个问题，我们需要分两部分来考虑：首先，用初始的10分钱购买桃子；其次，利用吃桃子后得到的桃核进行兑换，尽可能多地获取额外的桃子。

### 第一步：用10分钱购买桃子

1. 用10分钱可以购买10个桃子。
2. 吃掉这些桃子后，会得到10个桃核。

### 第二步：利用桃核兑换桃子

1. 每3个桃核可以兑换1个桃子，因此10个桃核可以兑换3个桃子。
2. 吃掉这3个桃子后，会得到3个桃核。
3. 用这3个桃核再兑换1个桃子，吃掉后得到1个桃核。
4. 最后剩下的1个桃核无法兑换桃子。

### 总结

- 初始购买：10个桃子
- 通过兑换桃核获得：3 + 1 = 4个桃子

因此，总共可以吃 \\(10 + 4 = 14\\) 个桃子。

这个分析考虑了所有可能的兑换机会，确保了最大化利用每一分钱和每个桃核。

Negative side arguing: 我同意你的分析过程，但需要进一步优化以确保我们没有遗漏任何可能的桃子获取途径。让我们重新审视整个过程，确保每一步都合理且最大化收益。

### 第一步：用10分钱购买桃子

1. 用10分钱可以购买10个桃子。
2. 吃掉这些桃子后，会得到10个桃核。

### 第二步：利用桃核兑换桃子

1. 每3个桃核可以兑换1个桃子，因此10个桃核可以兑换3个桃子。
2. 吃掉这3个桃子后，会得到3个桃核。
3. 用这3个桃核再兑换1个桃子，吃掉后得到1个桃核。
4. 最后剩下的1个桃核无法兑换桃子。

### 第三步：再次利用剩余桃核

1. 在第二步结束后，我们有1个桃核。如果能再次获得桃核，我们可以继续兑换桃子。
2. 为了再次获得桃核，我们需要再次购买桃子。用1分钱购买1个桃子，吃掉后得到1个桃核。
3. 现在我们有2个桃核，再兑换1个桃子，吃掉后得到1个桃核。
4. 现在我们有3个桃核，可以兑换1个桃子，吃掉后得到1个桃核。
5. 最后剩下的1个桃核无法兑换桃子。

### 总结

- 初始购买：10个桃子
- 通过兑换桃核获得：3 + 1 + 1 + 1 = 6个桃子

因此，总共可以吃 \\(10 + 6 = 16\\) 个桃子。

### 详细解释

1. **初始购买**：用10分钱购买10个桃子。
2. **第一次兑换**：10个桃核兑换3个桃子，吃掉后得到3个桃核。
3. **第二次兑换**：3个桃核兑换1个桃子，吃掉后得到1个桃核。
4. **第三次兑换**：1个桃核兑换1个桃子，吃掉后得到1个桃核。
5. **第四次兑换**：1个桃核兑换1个桃子，吃掉后得到1个桃核。

通过这种方法，我们确保了每一步都利用了所有的桃核进行兑换，从而最大化了桃子的总数。最终答案是16个桃子。
'''

    #resutl=classifyagent.classify_question(debate_topic)
    resutl=debatejudgment.evaluation(debate_text=debate_topic)
    print(resutl)
