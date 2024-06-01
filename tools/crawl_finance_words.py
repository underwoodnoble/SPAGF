import requests
import json
from pathlib import Path


def crawl(web_url: str, save_path: str) -> str:
    resp = requests.get(web_url)
    with open(save_path, 'w') as f:
        f.write(resp.text)

    return resp.text


def text_parser(text: str, save_path: str):
    concepts = []
    for line in text.split('\n'):
        index = line.find("<br><b>")
        if index == -1:
            continue
        concept_start = index + len('<br><b>')
        concept_end = line.find(':</b> ')
        if concept_end == -1:
            continue
        concept = line[concept_start:concept_end]
        meaning = line[concept_end + len(':</b> '):].strip()
        if len(concept.split(' ')) > 3 or '-' in concept or '(' in concept:
            continue
        concepts.append({"concept": concept, "meaning": meaning})
    
    with open(save_path, 'w') as f:
        json.dump(concepts, f, ensure_ascii=False, indent=2)


def main():
    web_url = "https://home.ubalt.edu/ntsbarsh/Business-stat/stat-data/KeysPhrasFinance.htm"
    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / 'data'
    if not data_dir.exists():
        data_dir.mkdir()
    text = crawl(web_url, data_dir / 'raw_page.html')
    text_parser(text, data_dir / 'concepts.json')


if __name__ == '__main__':
    main()