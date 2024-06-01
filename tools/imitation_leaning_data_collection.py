import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI


def get_response(messages: List):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"}
        ]
    )
    print(completion.model_dump_json())
    
    
if __name__ == '__main__':
    get_response()