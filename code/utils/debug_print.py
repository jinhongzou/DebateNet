import pprint
from datetime import datetime

is_debug = True 

def dprint(*args, **kwargs):
    """
    类似于 print 的调试打印函数，但是会为输出添加时间戳并使用 pprint 进行美化。
    
    :param args: 要打印的任意数量的参数
    :param kwargs: 可选关键字参数，传递给 pprint.pprint()
    """
    if is_debug:
        pp = pprint.PrettyPrinter(indent=2)
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        print(f"=== [{timestamp}] ===")

        for arg in args:
            if isinstance(arg, (dict, list, tuple)):
                pp.pprint(arg, **kwargs)
            else:
                print(arg)
        print("=== END ===\n")

# 示例用法
if __name__ == "__main__":
    model_name = "qwen-7b-instruct"
    messages = [
        {'role': 'system', 'content': "You are a debater. Hello and welcome to the debate..."},
        {'role': 'user', 'content': 'e '}
    ]
    temperature = 0.7
    max_tokens = 4045

    # 打印调试信息
    dprint("Request details:")
    dprint({
        "model_name": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })

    try:
        # 模拟 API 调用
        response = {
            "choices": [{"message": {"content": "This is a response from the model"}}],
            "other_info": "Some additional information"
        }
        
        # 成功响应后的调试信息
        dprint("Response details:")
        dprint(response)

    except Exception as e:
        # 错误发生时的调试信息
        dprint("Error details:")
        dprint({
            "status": "Error",
            "error_message": str(e),
        })