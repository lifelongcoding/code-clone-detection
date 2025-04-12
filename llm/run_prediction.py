from openai import OpenAI
from src.llm_predictor import load_config, load_prompt, setup_logger, get_predict
import os
from pathlib import Path
from datetime import datetime

if __name__ == '__main__':
    base_dir = Path(__file__).parent

    config = load_config(base_dir)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{config['model']}_{current_time}.log"
    logger = setup_logger(log_filename)
    prompt = load_prompt("java_clone_detect", base_dir)
    client = OpenAI(api_key=config['api_key'], base_url=config['base_url'])

    csv_file_dir = '../data/raw'
    csv_output_dir = f'../data/predict_{config["model"]}'

    for file_name in os.listdir(csv_file_dir):
        if file_name.endswith('.csv'):
            get_predict(csv_file_dir, file_name, csv_output_dir, client, config, prompt)
