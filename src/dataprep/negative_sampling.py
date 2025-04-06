import pandas as pd
import random


def generate_negative_clones(input_csv, output_csv, num_samples=500):
    df = pd.read_csv(input_csv)

    functions_1 = df[['FUNCTION_ID_ONE', 'FUNCTION_ONE_NAME', 'FUNCTION_ONE_TYPE',
                      'FUNCTION_ONE_STARTLINE', 'FUNCTION_ONE_ENDLINE', 'FUNCTIONALITY_ID']]
    functions_1.columns = ['FUNCTION_ID', 'FUNCTION_NAME', 'FUNCTION_TYPE', 'FUNCTION_STARTLINE', 'FUNCTION_ENDLINE', 'FUNCTIONALITY_ID']

    functions_2 = df[['FUNCTION_ID_TWO', 'FUNCTION_TWO_NAME', 'FUNCTION_TWO_TYPE',
                      'FUNCTION_TWO_STARTLINE', 'FUNCTION_TWO_ENDLINE', 'FUNCTIONALITY_ID']]
    functions_2.columns = ['FUNCTION_ID', 'FUNCTION_NAME', 'FUNCTION_TYPE', 'FUNCTION_STARTLINE', 'FUNCTION_ENDLINE', 'FUNCTIONALITY_ID']

    all_functions = pd.concat([functions_1, functions_2]).drop_duplicates().reset_index(drop=True)
    function_list = list(all_functions.itertuples(index=False))

    negative_pairs = []
    while len(negative_pairs) < num_samples:
        func1, func2 = random.sample(function_list, 2)
        if func1.FUNCTIONALITY_ID != func2.FUNCTIONALITY_ID:
            negative_pairs.append((
                func1.FUNCTION_ID, func1.FUNCTIONALITY_ID, func1.FUNCTION_NAME, func1.FUNCTION_TYPE,
                func1.FUNCTION_STARTLINE, func1.FUNCTION_ENDLINE,
                func2.FUNCTION_ID, func2.FUNCTIONALITY_ID, func2.FUNCTION_NAME, func2.FUNCTION_TYPE,
                func2.FUNCTION_STARTLINE, func2.FUNCTION_ENDLINE,
            ))

    pd.DataFrame(negative_pairs, columns=[
        'FUNCTION_ID_ONE', 'FUNCTIONALITY_ID_ONE',
        'FUNCTION_ONE_NAME', 'FUNCTION_ONE_TYPE', 'FUNCTION_ONE_STARTLINE', 'FUNCTION_ONE_ENDLINE',
        'FUNCTION_ID_TWO', 'FUNCTIONALITY_ID_TWO',
        'FUNCTION_TWO_NAME', 'FUNCTION_TWO_TYPE', 'FUNCTION_TWO_STARTLINE', 'FUNCTION_TWO_ENDLINE',
    ]).to_csv(output_csv, index=False)
    print(f"[+] Generated {len(negative_pairs)} negative clone pairs to {output_csv}")
