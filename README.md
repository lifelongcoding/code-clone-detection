# **Code Clone Detection**

## **Introduction**

This repository was created as part of a graduation project to evaluate the performance of large language models (LLMs) and pretrained models(CodeBERT etc.) in the task of code clone detection.

---

## **Data preparation**

I used the latest versions of BigCloneBench and IJaDataset, which can be downloaded via [BigCloneEval](https://github.com/jeffsvajlenko/BigCloneEval). Due to limitations in both budget and time, I was only able to utilize a small subset of these datasets for testing.

---

### Extracting Useful Information from H2 Database into CSV Files

I used SQL commands to extract useful information into a CSV file. For example, this [SQL script](scripts/Extract_VST3_Clones.sql) extracts **500 Very-Strongly Type-3 (VST3) code pairs** along with their **corresponding file paths** from the database. You can modify certain parameters in this script to extract different types and quantities of code pairs.

- `SYNTACTIC_TYPE`: The type of code pair

- `SIMILARITY_LINE`: The syntactic similarity at the line level (ranging from 0 to 1). This is used to differentiate clone types.

  > **Very-Strongly Type-3 (VST3)**: Similarity between **90% (inclusive) and 100%**.
  >
  > **Strongly Type-3 (ST3)**: Similarity between **70% and 90%**.
  >
  > **Moderately Type-3 (MT3)**: Similarity between **50% and 70%**.
  >
  > **Weakly Type-3 or Type-4 (WT3/4)**: Similarity between **0% and 50%**.

The extracted CSV files are stored in:  

📂 `data/ref`  

**Note:** This data only provides references to function locations. The actual source files containing the functions reside in the **IJaDataset**.  

---

### **Extracting Actual Functions from IJaDataset**

After extracting metadata from the **BigCloneBench dataset** in the previous step, the next step is to locate the actual function implementations in the **IJaDataset dataset** and save them into a new CSV file.

#### **Output Format**

The resulting CSV file will contain the following fields:

- **`FUNCTION_ONE`**: The source code of the first function.
- **`FUNCTION_TWO`**: The source code of the second function.
- **`LABEL`**: Default value is `1` since **BigCloneBench** is a fully positive dataset (all pairs represent code clones).

The extracted CSV files are stored in:  

📂 `data/raw  

#### **Extraction Process**

To extract the actual functions, use the provided script:

```shell
python /scripts/extract_functions.py
```

You can modify parameters in `extract.py` to customize the extraction process based on your requirements.
