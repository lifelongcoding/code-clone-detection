from src.dataprep import batch_extract_from_dir


batch_extract_from_dir(
    input_dir="../data/ref/",
    output_dir="../data/raw/",
    base_code_path=r"/path/to/IJaDataset_BCEvalVersion/bcb_reduced",
    label=1)

batch_extract_from_dir(
    input_dir="../data/ref_neg/",
    output_dir="../data/raw_neg/",
    base_code_path=r"/path/to/IJaDataset_BCEvalVersion/bcb_reduced",
    label=0)
