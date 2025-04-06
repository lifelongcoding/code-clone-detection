import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_recall_bar(file_paths, labels, title="Recall per Clone Type", ylim=(0, 1.1), palette="Greens"):
    results = []

    for path, label in zip(file_paths, labels):
        df = pd.read_csv(path)
        recall = df["PREDICT"].mean()
        fn_count = (df["PREDICT"] == 0).sum()
        results.append({"Type": label, "Recall": recall, "FN Count": fn_count})

    results_df = pd.DataFrame(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=results_df, x="Type", y="Recall", hue="Type", palette=palette, legend=False)
    plt.title(title)
    plt.ylim(*ylim)

    for index, row in results_df.iterrows():
        plt.text(index, row.Recall + 0.02, f"{row.Recall:.2%}\nFN: {row['FN Count']}", ha="center")

    plt.show()
