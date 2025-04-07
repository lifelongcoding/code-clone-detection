import os
import pandas as pd
import logging

logger = logging.getLogger()


def get_predict(input_dir, csv_file_name, output_dir, client, config, prompt):
    input_path = os.path.join(input_dir, csv_file_name)
    df = pd.read_csv(input_path)
    logger.info(f"Processing file：{csv_file_name}")
    df['PREDICT'] = None

    total_file_tokens = 0
    for index, row in df.iterrows():
        try:
            response = client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"CODE_FRAGMENT1: {row['FUNCTION_ONE']}\nCODE_FRAGMENT2: {row['FUNCTION_TWO']}"},
                ],
                stream=False,
                temperature=0.1
            )

            prediction = response.choices[0].message.content.lstrip("\n")
            df.at[index, 'PREDICT'] = prediction

            if hasattr(response.choices[0].message, "reasoning_content"):
                cot = response.choices[0].message.reasoning_content
                df.at[index, 'COT'] = cot

            usage = response.usage
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            cached_tokens = usage.prompt_tokens_details.cached_tokens
            reasoning_tokens = usage.completion_tokens_details.reasoning_tokens

            logger.info(
                f"Processed row {index + 1}/{len(df)}, predict: {prediction}, "
                f"Total Tokens: {total_tokens}, Prompt Tokens: {prompt_tokens}, "
                f"Completion Tokens: {completion_tokens}, Cached Tokens: {cached_tokens}, "
                f"Reasoning Tokens: {reasoning_tokens}"
            )

            total_file_tokens += total_tokens
        except Exception as e:
            logger.error(f"Error processing row {index + 1}: {e}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, csv_file_name)
    df.to_csv(output_path, index=False)
    logger.info(f"Finished processing {csv_file_name}, Total tokens used: {total_file_tokens}")
