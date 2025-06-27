

from typing import Literal
import dspy

import dspy


class Classify(dspy.Signature):
    """Classify sentiment of a given classify."""
    context: str = dspy.InputField()
    Category: Literal['Discussion', 'Answer'] = dspy.OutputField(desc=
"""
### 讨论类（Discussion）

**适用情况**：
用户明确或隐含地要求进行深入分析、多角度思考等。或者这类问题可能引发多角度的思考、推理、建模、策略制定、情境判断或现实应用探讨，即使表面看似简单，也可能引出深层次的讨论。适合用于激发思维、引导分析、促进交流。

在以下情况下归为此类：
- 用户明确或隐含地要求进行讨论、分析、推理、建模或多角度思考等
- 即使存在唯一答案，也需要一定思维过程
- 能够拓展到教学、现实应用、编程实现等场景
- 没有唯一正确答案

**典型示例**：
- “你觉得人工智能对教育的影响是积极还是消极的？”
- “如果全球气温继续上升，我们应该如何应对？”
- “如果每天减少10%的碳排放，一年后会有什么影响？”
- “**请分析**， 你喝掉了一杯牛奶的20%。然后你将杯子加满水，再喝掉了其中的40%，然后再一次将杯子加满水。现在这杯中牛奶的百分比是多少？”

### 直接回答类（Answer）

**适用情况**：  
该类问题或语句具有明确的答案，或者不构成实质性提问的问候语，可以通过简短的事实性信息直接回应，无需进一步探讨或推理。

仅在以下情况下归为此类：
- 明确的事实性问题（如时间、人物、地点、定义）
- 不构成提问的问候语（如“你好”）
- 答案可以在一步内从常识或数据中提取
- 问题只需一步常识或事实即可回答，无需推理或深入分析。

**典型示例**：
- “今天星期几？”
- “谁写了《红楼梦》？”
- “光的速度是多少？”
- “你好”
- “法国的首都是哪座城市？”

""")
    #reason: str = dspy.OutputField(desc="""判断属于哪一类的理由""")
    Answer: str = dspy.OutputField(desc="""回答的答案""")

from dspy import Signature, OutputField, InputField
from typing import Literal, Optional

class ModeratorEvaluationOutDSPy(Signature):
    """
    Analyze both sides of the current situation and provide a comprehensive final answer.
    
    The output should indicate which position is more reasonable and integrate insights from both sides.
    """

    debate_context: str = InputField(
        desc="Full debate content comprising arguments from both Affirmative and Negative perspectives."
    )

    supported_side: Literal['Affirmative', 'Negative', 'Neither'] = OutputField(
        desc="The side you support based on the analysis. Choose from 'Affirmative', 'Negative', or 'Neither'."
    )
    reason: str = OutputField(
        desc="Your detailed analysis of the situation and why you support a certain position."
    )

from pydantic import BaseModel
from pydantic import field_validator

class ModeratorEvaluationOut(BaseModel):
    #whether_there_is_a_preference: Literal['Yes', 'No']
    supported_side: Literal['Affirmative', 'Negative','Neutral']
    reason: Optional[str] = None
    #debate_answer: Optional[str] = None

    @field_validator('reason', mode='before')
    def clean_reason(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return None
        return v

class JudgeEvaluationOut(BaseModel):
    """
    Analyze both sides of the current situation and provide a comprehensive final answer.
    
    The output should indicate which position is more reasonable and integrate insights from both sides.
    """

    reasoning: Optional[str] = None
    supported_side: Literal['Affirmative', 'Negative']
    final_answer: Optional[str] = None

    @field_validator('reasoning', mode='before')
    def clean_reason(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return None
        return v

    @field_validator('final_answer', mode='before')
    def clean_final_answer(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return None
        return v