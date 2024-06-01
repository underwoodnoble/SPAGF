import os
import argparse
from typing import List

from dotenv import load_dotenv
from openai import OpenAI


def set_api(model, temperature):
    def get_response(messages: List) -> str:
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        return resp.to_dict()['choices'][0]['message']['content']
    return get_response


def main(args):
    print(get_response([{"role": "user", "content": "请问你是谁？"}]))


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        type=str,
        default='qwen-turbo',
        choices=['qwen-turbo']
    )
    parser.add_argument(
        '--concept_path',
        type=str
    )
    parser.add_argument(
        '--save_path',
        type=str
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=1.0
    )
    parser.add_argument(
        '--max_concept_length',
        type=int,
        default=3,
        help="Maximum number of words in a concept."
    )
    args = parser.parse_args()
    get_response = set_api(args.model, args.temperature)
    main(args)