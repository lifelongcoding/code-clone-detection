import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


def load_label_from_dir(directory):
    y_pred, y_true = [], []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        df = pd.read_csv(filepath)
        y_pred.extend(df['PREDICT'].tolist())
        y_true.extend(df['LABEL'].tolist())
    return y_pred, y_true


def evaluate_metrics(y_true, y_pred, average='binary'):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average=average, zero_division=0)
    recall = recall_score(y_true, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=average, zero_division=0)
    return accuracy, precision, recall, f1


def evaluate_and_print_metrics(y_true, y_pred, title):
    accuracy, precision, recall, f1 = evaluate_metrics(y_true, y_pred)
    print(f"=== {title} ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}\n")


def plot_single_confusion_matrix(y_true, y_pred, title, subplot_index=None):
    cm = confusion_matrix(y_true, y_pred)
    labels = sorted(set(y_true) | set(y_pred))

    if subplot_index is not None:
        plt.subplot(1, 2, subplot_index)

    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(title)


def plot_confusion_matrix(directories, title, subplot_index):
    y_pred, y_true = [], []
    for directory in directories:
        pred, true = load_label_from_dir(directory)
        y_pred.extend(pred)
        y_true.extend(true)

    evaluate_and_print_metrics(y_true, y_pred, title)
    plot_single_confusion_matrix(y_true, y_pred, title, subplot_index=subplot_index)
