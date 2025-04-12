import os
from datetime import datetime
import torch
from torch.nn.functional import cosine_similarity
from transformers import AutoModel, AutoTokenizer
import pandas as pd
from src.llm_predictor import setup_logger
from tqdm import tqdm

from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# CSV_FILE_DIR = BASE_DIR / 'data' / 'raw_neg'
# OUTPUT_FILE_DIR = BASE_DIR / 'data' / 'predict_neg_codebert_test'
#
# MODEL_PATH = BASE_DIR / 'model' / 'codebert-base'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_DIR = os.path.join(BASE_DIR, '../data/raw')
OUTPUT_FILE_DIR = os.path.join(BASE_DIR, '../data/predict_codebert')

MODEL_PATH = os.path.join(BASE_DIR, '../models/codebert-base')

MAX_SEQ_LENGTH = 512
BATCH_SIZE = 16


def calculate_embeddings_in_batches(code_list, model, tokenizer, device, batch_size, max_length):
    model.eval()
    all_embeddings = []
    num_samples = len(code_list)
    logger.info(f"Calculating embeddings for {num_samples} code snippets in batches of {batch_size}...")
    for i in tqdm(range(0, num_samples, batch_size)):
        batch_code = code_list[i:i+batch_size]
        inputs = tokenizer(batch_code, return_tensors='pt', padding=True, truncation=True, max_length=max_length)
        inputs = {k: v.to(device) for k, v in inputs.items()}  # 移动到设备
        with torch.no_grad():
            batch_embeddings = model(**inputs).last_hidden_state[:, 0, :]
        all_embeddings.append(batch_embeddings.cpu())
    logger.info("Embedding calculation finished.")
    return torch.cat(all_embeddings, dim=0)


if __name__ == '__main__':
    os.makedirs(OUTPUT_FILE_DIR, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"codebert_{current_time}.log"
    logger = setup_logger(log_filename)

    logger.info("Starting Code Similarity Calculation...")
    logger.info(f"CSV Source Directory: {CSV_FILE_DIR}")
    logger.info(f"Output Directory: {OUTPUT_FILE_DIR}")
    logger.info(f"Model Path: {MODEL_PATH}")

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")

        logger.info("Loading model and tokenizer...")
        model = AutoModel.from_pretrained(MODEL_PATH, local_files_only=True).to(device)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
        logger.info("Model and tokenizer loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading model or tokenizer: {e}", exc_info=True)
        exit(1)

    for file in os.listdir(CSV_FILE_DIR):
        if file.endswith('.csv'):
            file_path = os.path.join(CSV_FILE_DIR, file)
            output_path = os.path.join(OUTPUT_FILE_DIR, file)
            logger.info(f"Processing file: {file_path}")

            try:
                df = pd.read_csv(file_path)
                logger.info(f"Read {len(df)} rows from {file}")

                if 'FUNCTION_ONE' not in df.columns or 'FUNCTION_TWO' not in df.columns:
                    logger.warning(f"Skipping {file}: Columns 'FUNCTION_ONE' or 'FUNCTION_TWO' not found.")
                    continue

                df['FUNCTION_ONE'].fillna("[EMPTY]", inplace=True)
                df['FUNCTION_TWO'].fillna("[EMPTY]", inplace=True)

                code_list_1 = df['FUNCTION_ONE'].tolist()
                code_list_2 = df['FUNCTION_TWO'].tolist()

                embeddings_1 = calculate_embeddings_in_batches(code_list_1, model, tokenizer, device, BATCH_SIZE, MAX_SEQ_LENGTH)
                embeddings_2 = calculate_embeddings_in_batches(code_list_2, model, tokenizer, device, BATCH_SIZE, MAX_SEQ_LENGTH)

                logger.info("Calculating cosine similarities...")
                similarities = cosine_similarity(embeddings_1, embeddings_2).numpy()
                logger.info("Similarity calculation finished.")

                df['SIMILARITY'] = similarities
                df.to_csv(output_path, index=False)
                logger.info(f"Saved results with similarities to: {output_path}")

            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")
            except pd.errors.EmptyDataError:
                logger.warning(f"File is empty, skipping: {file_path}")
            except Exception as e:
                logger.error(f"An error occurred while processing {file}: {e}", exc_info=True)

    logger.info("Processing finished.")