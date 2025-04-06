import os
import pandas as pd
import linecache


def extract_method(file_path, start_line, end_line):
    """Extracts method code from the specified file between given line numbers."""
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return ""
    return "\n".join([linecache.getline(file_path, i).rstrip() for i in range(start_line, end_line + 1)])


def extract_function_pairs_from_csv(input_csv, output_csv, base_code_path, label):
    df = pd.read_csv(input_csv)
    new_data = []
    is_negative = (label == 0)

    for _, row in df.iterrows():
        fid_one = row["FUNCTIONALITY_ID_ONE"] if is_negative else row["FUNCTIONALITY_ID"]
        fid_two = row["FUNCTIONALITY_ID_TWO"] if is_negative else row["FUNCTIONALITY_ID"]

        func_one_path = os.path.join(base_code_path, str(fid_one), row["FUNCTION_ONE_TYPE"], row["FUNCTION_ONE_NAME"])
        func_two_path = os.path.join(base_code_path, str(fid_two), row["FUNCTION_TWO_TYPE"], row["FUNCTION_TWO_NAME"])

        func1 = extract_method(func_one_path, row["FUNCTION_ONE_STARTLINE"], row["FUNCTION_ONE_ENDLINE"])
        func2 = extract_method(func_two_path, row["FUNCTION_TWO_STARTLINE"], row["FUNCTION_TWO_ENDLINE"])

        new_data.append([func1, func2, label])

    pd.DataFrame(new_data, columns=["FUNCTION_ONE", "FUNCTION_TWO", "LABEL"]).to_csv(output_csv, index=False)
    print(f"[+] Extracted and saved to {output_csv}")


def batch_extract_from_dir(input_dir, output_dir, base_code_path, label):
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            input_csv = os.path.join(input_dir, file_name)
            output_csv = os.path.join(output_dir, file_name)
            print(f"[*] Processing {file_name}...")
            extract_function_pairs_from_csv(input_csv, output_csv, base_code_path, label)
