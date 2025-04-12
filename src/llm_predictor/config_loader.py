from configparser import ConfigParser
from pathlib import Path


def load_config(base_dir: Path) -> dict:
    config = ConfigParser()
    config.read(base_dir / 'config' / 'config.ini')
    return {
        'api_key': config['API']['api_key'],
        'base_url': config['API']['base_url'],
        'model': config['API']['model']
    }


def load_prompt(prompt_name: str, base_dir: Path) -> str:
    prompt_path = base_dir / 'config' / 'prompts' / f'{prompt_name}.md'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()
