from src.evaluation_plotter import plot_recall_bar
from src.evaluation_plotter import plot_confusion_matrix
import matplotlib.pyplot as plt


labels = ["T1", "T2", "VST3", "ST3", "MT3", "WT3_4"]
file_paths_1 = [f"../data/predict_v3/{name}.csv" for name in labels]
file_paths_2 = [f"../data/predict_r1/{name}.csv" for name in labels]

plot_recall_bar(file_paths_1, labels, title="Recall per Clone Type (DeepSeek-V3)")
plot_recall_bar(file_paths_2, labels, title="Recall per Clone Type (DeepSeek-R1)")

plt.figure(figsize=(12, 6))
plot_confusion_matrix(["../data/predict_v3_neg", "../data/predict_v3"], "Confusion Matrix (DeepSeek-V3)", 1)
plot_confusion_matrix(["../data/predict_r1_neg", "../data/predict_r1"], "Confusion Matrix (DeepSeek-R1)", 2)
plt.tight_layout()
plt.show()
