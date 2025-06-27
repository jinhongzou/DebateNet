
from pydantic_ai import Agent,  ToolOutput
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIModel

import dspy
from typing import Optional,Union
 
from .debug_logfire import logfire
from .models import Classify, ModeratorEvaluationOutDSPy
from pydantic_ai.tools import RunContext  

class Classifier:
    def __init__(
        self,
        model: str,
        api_key: str,
        api_base: Optional[str] = None,
        name: str='Classifier',
    ) -> None:
        """
        Initialize a classification agent that uses DSPy to classify questions.

        Args:
            model (Agent): The model name or configuration.
            api_key (str): API key for the language model service.
            api_base (Optional[str]): Base URL for the API (e.g., Azure or custom OpenAI endpoint).
        """
        # 初始化语言模型
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            api_base=api_base
        )
        self.name = name
        # 设置全局默认语言模型
        # dspy.settings.configure(lm=self.lm )

    def classify_question(self, context: str) -> str:
        """
        Classifies the given question using a DSPy Predict module.

        Args:
            question (str): Input question to be classified.

        Returns:
            str: Classification result.
        """
        try:
            
            with dspy.context(lm = self.lm): 
                predict_module = dspy.Predict(Classify)
                #predict_module = dspy.ChainOfThought(Classify)
                result = predict_module(context=context)
                logfire.info(f'{self.name} run',  context=self.lm.history[-1] if self.lm.history else None)

                return result  # 假设返回结果字段是 answer
        except Exception as e:
            print(f"Error during classification: {e}")
            return "unknown"

# 定制评估函数
class Evaluator:
    def __init__(
        self,
        model: str,
        api_key: str ,
        api_base: str,
        signature: str,
        instructions: Optional[str] = None,
        name: str='Evaluator'
    ) -> None:
        """
        Initialize a classification agent that uses DSPy to classify questions.

        Args:
            model (Agent): The model name or configuration.
            api_key (str): API key for the language model service.
            api_base (Optional[str]): Base URL for the API (e.g., Azure or custom OpenAI endpoint).
        """
        # 初始化语言模型
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            api_base=api_base
        )
        self.signature = signature
        self.instructions = instructions
        self.name = name
        # 设置全局默认语言模型
        # dspy.settings.configure(lm=self.lm )

    def run(self, **kwargs) -> str:
        """
        Classifies the given question using a DSPy Predict module.

        Args:
            question (str): Input question to be classified.

        Returns:
            str: Classification result.
        """
        try:
            with dspy.context(lm = self.lm): 
                signature = dspy.Signature(signature=self.signature, instructions=self.instructions)
                classify = dspy.Predict(signature)
                result = classify(**kwargs)
                logfire.info(f'{self.name} run',  context=self.lm.history[-1] if self.lm.history else None)
                return result # 假设返回结果字段是 answer

        except Exception as e:
            print(f"Error during classification: {e}")
            return "unknown"

class Moderator:
    def __init__(
        self,
        model: str,
        api_key: str,
        api_base: Optional[str] = None,
        name: str='Moderator',
    ) -> None:
        """
        Initialize a classification agent that uses DSPy to classify questions.

        Args:
            model (Agent): The model name or configuration.
            api_key (str): API key for the language model service.
            api_base (Optional[str]): Base URL for the API (e.g., Azure or custom OpenAI endpoint).
        """
        # 初始化语言模型
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            api_base=api_base
        )
        self.name = name
        # 设置全局默认语言模型
        # dspy.settings.configure(lm=self.lm )

    def run(self, debate_context: str) -> str:
        """
        Classifies the given question using a DSPy Predict module.

        Args:
            question (str): Input question to be classified.

        Returns:
            str: Classification result.
        """
        try:

            with dspy.context(lm = self.lm): 
                predict_module = dspy.Predict(ModeratorEvaluationOutDSPy)
                #predict_module = dspy.ChainOfThought(ModeratorEvaluationOutDSPy)
                result = predict_module(debate_context=debate_context)

                logfire.info(f'{self.name} run',  context=self.lm.history[-1] if self.lm.history else None)
                #print(self.lm.history[-1] if self.lm.history else None)
                return result  # 假设返回结果字段是 answer
        except Exception as e:
            print(f"Error during evaluation: {e}")
            return "unknown"



from typing import TypeVar
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelRequestPart, ModelResponse, TextPart, UserPromptPart

OutputDataT = TypeVar("OutputDataT")

class PydanticAgent():
    def __init__(
        self,
        name: str,
        model: OpenAIModel, 
        output_type: type[OutputDataT] | ToolOutput[OutputDataT],
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        """
        Create an agent

        """
        #self.memory_lst = []
        self.name = name
        
        # 判断的是历史all_messages()的context上下文内容
        def completion_detector_hook(messages: list[ModelMessage]) -> list[ModelMessage]:  
            """检测完成标记并处理任务结束"""  
            for message in messages:  
                #print (f">>>> message:  {message} <<<<")
                if isinstance(message, ModelResponse):  
                    for part in message.parts:  
                        #print (f">>>> Part:  {part} <<<<")
                        if isinstance(part, TextPart) and part.content.strip() == "[[ ## completed ## ]]":  
                            # 找到完成标记，可以在这里添加结束逻辑  
                            # 例如：抛出自定义异常来停止执行  
                            print("任务已完成.........")
                            raise TaskCompletedException("任务已完成")

            return messages
        
        class TaskCompletedException(Exception):  
            """任务完成异常"""  
            pass

        self.agent = Agent(model=model, 
                           name=name, 
                           output_type=output_type,
                           system_prompt=system_prompt,
                           model_settings={'tool_choice': 'auto'},
                           retries=3,
                           history_processors=[completion_detector_hook]
                           )
    
        self.message_history: list[ModelMessage] = []
        self.last_answer=''

    def ask(self, question: str, reset_history=True, max_msg:int=10) -> str:
        
        if self.message_history == None or reset_history==True:
            result = self.agent.run_sync(
            user_prompt=question,
        )
        else:
            result = self.agent.run_sync(
            user_prompt=question,
            message_history= self.message_history[-max_msg:] if len(self.message_history) > max_msg else self.message_history
        )

        self.message_history=result.all_messages()
        self.last_answer=result.output
        
        return result.output
    '''
    def add_event(self, event: str):
        """Add an new event in the memory

        Args:
            event (str): string that describe the event.
        """
        self.message_history.append({"role": "user", "content": f"{event}"})

    def _add_memory(self, memory: str):
        """Monologue in the memory

        Args:
            memory (str): string that generated by the model in the last round.
        """
        self.message_history.append({"role": "assistant", "content": f"{memory}"})
        print(f"----- {self.name} memory: \n{self.message_history} -----\n")

    def ask(self, question: str):

        answer = self._query(question)
        #self._add_memory(answer)
        return answer
    '''
    def get_all_messages(self):
        """Get the memory of the agent"""
        return self.message_history
