import json
import numpy as np
import time
import joblib

from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# =========================
# Load Dataset
# =========================
print("Loading dataset...")
with open("evaluation/malicious_prompt_dataset.json", "r") as f:
    data = json.load(f)

prompts = [item["prompt"] for item in data]
labels = [item["label"] for item in data]

print("Dataset size:", len(labels))
print("Class distribution:", Counter(labels))

if len(set(labels)) < 2:
    raise ValueError("Dataset must contain both classes (0 and 1).")

# =========================
# Load Embedding Model
# =========================
print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# Generate Embeddings
# =========================
print("Generating embeddings...")
start = time.time()
embeddings = model.encode(prompts)
embedding_time = (time.time() - start) * 1000
print(f"Embedding generation time: {embedding_time:.2f} ms")

# =========================
# Train / Test Split
# =========================
print("\nSplitting dataset (stratified)...")
X_train, X_test, y_train, y_test = train_test_split(
    embeddings,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)

# =========================
# Train Classifier
# =========================
print("Training logistic regression classifier...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# =========================
# Evaluate
# =========================
print("\nEvaluating model...")

# Use probability-based decision
y_probs = clf.predict_proba(X_test)[:, 1]
threshold = 0.5
y_pred = (y_probs >= threshold).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

print("\n=== Injection Detection Evaluation ===")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print(f"\nFalse Positive Rate (FPR): {fpr:.4f}")
print(f"False Negative Rate (FNR): {fnr:.4f}")

print("\nProbability Stats:")
print("Min:", np.min(y_probs))
print("Max:", np.max(y_probs))
print("Mean:", np.mean(y_probs))

# =========================
# Threshold Sweep
# =========================
print("\nThreshold Sweep:")
for t in [0.3, 0.4, 0.5, 0.6, 0.7]:
    preds = (y_probs >= t).astype(int)
    p = precision_score(y_test, preds)
    r = recall_score(y_test, preds)
    cm_temp = confusion_matrix(y_test, preds)
    tn_, fp_, fn_, tp_ = cm_temp.ravel()
    fpr_ = fp_ / (fp_ + tn_) if (fp_ + tn_) > 0 else 0
    print(f"Threshold {t} -> Precision: {p:.3f}, Recall: {r:.3f}, FPR: {fpr_:.3f}")

# =========================
# Save Model + Report
# =========================
report = {
    "dataset_size": len(labels),
    "class_distribution": dict(Counter(labels)),
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "fpr": fpr,
    "fnr": fnr,
    "embedding_time_ms": embedding_time,
    "confusion_matrix": cm.tolist(),
}

with open("evaluation/evaluation_report.json", "w") as f:
    json.dump(report, f, indent=4)

joblib.dump(clf, "evaluation/injection_model.pkl")

print("\nModel saved to evaluation/injection_model.pkl")
print("Evaluation report saved to evaluation/evaluation_report.json")
