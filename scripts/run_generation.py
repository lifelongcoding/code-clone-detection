from src.dataprep import generate_negative_clones
import os


csv_file_dir = '../data/ref'
csv_output_dir = '../data/ref_neg'

for file_name in os.listdir(csv_file_dir):
    os.makedirs(csv_output_dir, exist_ok=True)

    if file_name.endswith('.csv'):
        input_path = os.path.join(csv_file_dir, file_name)
        output_path = os.path.join(csv_output_dir, file_name)
        generate_negative_clones(input_path, output_path)