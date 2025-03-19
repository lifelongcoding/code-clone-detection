import pandas as pd
import os
import linecache


def extract_method(file_path, start_line, end_line):
    """Extracts method code from the specified file between given line numbers."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    method_lines = [linecache.getline(file_path, i).rstrip() for i in range(start_line, end_line + 1)]
    return "\n".join(method_lines)


# Define dataset base path (modify as needed)
BASE_DATASET_PATH = "/path/to/IJaDataset_BCEvalVersion/bcb_reduced"  # Update this path accordingly

# Input and output CSV paths
input_csv = "../data/ref/T2.csv"  # Update this path accordingly
output_csv = "../data/raw/T2.csv"

# Read the original CSV file
df = pd.read_csv(input_csv)

# Store extracted function data
new_data = []

for _, row in df.iterrows():
    # Construct file paths for both functions
    func_one_path = os.path.join(BASE_DATASET_PATH, str(row["FUNCTIONALITY_ID"]), row["FUNCTION_ONE_TYPE"], row["FUNCTION_ONE_NAME"])
    func_two_path = os.path.join(BASE_DATASET_PATH, str(row["FUNCTIONALITY_ID"]), row["FUNCTION_TWO_TYPE"], row["FUNCTION_TWO_NAME"])

    # Extract function code
    function_one_code = extract_method(func_one_path, row["FUNCTION_ONE_STARTLINE"], row["FUNCTION_ONE_ENDLINE"])
    function_two_code = extract_method(func_two_path, row["FUNCTION_TWO_STARTLINE"], row["FUNCTION_TWO_ENDLINE"])

    # Append extracted data (LABEL is set to 1)
    new_data.append([function_one_code, function_two_code, 1])

# Save extracted data to a new CSV file
new_df = pd.DataFrame(new_data, columns=["FUNCTION_ONE", "FUNCTION_TWO", "LABEL"])
new_df.to_csv(output_csv, index=False)

print(f"Processing complete. Results saved to {output_csv}")
