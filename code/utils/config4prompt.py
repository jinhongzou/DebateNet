### 基础信息字段
debate_topic = ""  # 辩论主题，当前为空
base_answer = ""   # 基础答案，当前为空
debate_answer = "" # 辩论最终结论，当前为空

### 辩手角色提示模板（Meta Prompt）
# modify by zoujinhong 20250626
player_meta_prompt = """You are a debater. Welcome to the debate.

Our goal is to find the correct answer, and you are encouraged to challenge commonly accepted views or newly proposed conclusions.

Your responsibilities include:
- Never easily accepting the other side's conclusion;
- Identifying logical flaws, counterexamples, or alternative interpretations;
- Supporting your position with clear, concise reasoning and examples;
- Maintaining a firm, rational, and efficient tone.

"""

### 主持人角色提示模板（Moderator Meta Prompt）
moderator_meta_prompt = """You are a moderator. There will be two debaters involved in a debate. They will present their answers and discuss their perspectives on the following topic: "##debate_topic##"
At the end of each round, you will evaluate answers and decide which is correct."""


### 正方提问模板（Affirmative Prompt）
affirmative_prompt = """ ##debate_topic## """


### 反方提问模板（Negative Prompt）
negative_prompt = """
[[ ## The debate topic  ## ]]
##debate_topic##

[[ Affirmative side arguing ]]
##aff_ans##


You are in a debate. Your task is to either:
1. You disagree with my answer. Provide a new, meaningful counterargument with reasons, OR
2. If you have absolutely no new argument, reply **ONLY** with: `[[ ## completed ## ]]`

⚠️ DO NOT include both a counterargument AND the completed tag in the same response.
"""

### 主持人评估模板（Moderator Prompt） (需要优化)
# modify by zoujinhong 20250626
moderator_prompt = """Now the ##round## round of debate for both sides has ended.

[[ Affirmative side arguing ]]
##aff_ans##

[[ Negative side arguing ]]
##neg_ans##

You, as the moderator, will evaluate both sides' arguments and apply a strict elimination process:

- If ONE side presents clearly superior reasoning, stronger evidence, and more persuasive logic, then:
  - Set "supported_side" to either "Affirmative" or "Negative", depending on which side you support.
  - Summarize your evaluation in "reason".
  - The debate will END here.

- If NEITHER side presents a clearly superior argument, then:
  - Set "supported_side" to "Neither".
  - Explain why neither side convinced you in "reason".
  - The debate will proceed to the next round.

Please respond strictly in plain text using the following format:

supported_side: Affirmative, Negative, or Neither
reason: [Your detailed evaluation]

Example:
supported_side: Affirmative
reason: The Affirmative side provided more compelling arguments based on current economic trends."""

### 辩论交互提示（Debate Prompt）
debate_prompt = """##oppo_ans##\n\nDo you agree with my perspective? Please provide your reasons and answer."""
debate_prompt_loop = """
##oppo_ans##


Do you agree with this perspective? Please generate a new and comprehensive counterargument to the above perspective.  
Your task is to either:
1. You disagree with my answer. Provide a new, meaningful counterargument with reasons, OR
2. If you have absolutely no new argument, reply **ONLY** with: `[[ ## completed ## ]]`

⚠️ DO NOT include both a counterargument AND the completed tag in the same response."""

    
# DSPy的prompt
# create by zoujinhong 20250626
judge_evaluator_prompt='''
[[ ## debate_topic ## ]]
##debate_topic##

[[ ## affirmative_side_arguing ## ]]
##affirmative_side_arguing##

[[ ## negative_side_arguing ## ]]
##negative_side_arguing##

'''

final_answer_prompt='''
##context##

[[ ## user question ## ]]
##user_question##

'''

# =============================================================================================
# 函数定义：将变量打包成 JSON 字符串
# 支持两种模式：
# - 不传参时使用全局变量
# - 传入自定义值时使用自定义值
# =============================================================================================
import json

def debate_prompt_json(
    debate_topic=debate_topic,
    base_answer=base_answer,
    debate_answer=debate_answer,
    player_meta_prompt=player_meta_prompt,
    moderator_meta_prompt=moderator_meta_prompt,
    affirmative_prompt=affirmative_prompt,
    negative_prompt=negative_prompt,
    moderator_prompt=moderator_prompt,
    judge_evaluator_prompt=judge_evaluator_prompt,
    final_answer_prompt=final_answer_prompt,
    debate_prompt= debate_prompt,
    debate_prompt_loop=debate_prompt_loop,
):
    """
    将各个辩论组件合并为一个 JSON 格式的字典。
    
    参数说明：
        所有参数都有默认值，如果不传则使用全局定义的默认模板；
        也可以传入自定义内容进行替换。
        
    返回值：
        JSON 格式的字符串（美化格式、支持中文字符）
    """
    debate_dict = {
        "debate_topic": debate_topic,
        "base_answer": base_answer,
        "debate_answer": debate_answer,
        "player_meta_prompt": player_meta_prompt,
        "moderator_meta_prompt": moderator_meta_prompt,
        "affirmative_prompt": affirmative_prompt,
        "negative_prompt": negative_prompt,
        "moderator_prompt": moderator_prompt,
        "judge_evaluator_prompt": judge_evaluator_prompt,
        "final_answer_prompt": final_answer_prompt,
        "debate_prompt": debate_prompt,
        "debate_prompt_loop": debate_prompt_loop,
    }
    #return json.dumps(debate_dict, indent=4, ensure_ascii=False)
    return debate_dict

# 示例用法：
# json_output = debate_prompt_json()
# print(json_output)
