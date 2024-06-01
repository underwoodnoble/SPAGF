import os
import argparse
import json
from typing import List, Dict, Callable
from pydantic import BaseModel

from dotenv import load_dotenv
from openai import OpenAI


def set_api(model: str, temperature: float) -> Callable[[List[Dict[str, str]]], str]:
    def get_response(messages: List[Dict[str, str]]) -> str:
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


class Concept(BaseModel):
    concept: str
    meaning: str


def load_concepts(concept_path: str) -> List[Concept]:
    with open(concept_path, 'r') as f:
        dataset = json.load(f)
    return [Concept(concept=data['concept'].strip().lower(), meaning=data['meaning'])
            for data in dataset]


def main(args):
    concepts = load_concepts(args.concept_path)
    print(concepts[0])


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