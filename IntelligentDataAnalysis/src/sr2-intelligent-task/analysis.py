import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from datetime import datetime

df = pd.read_csv("data/sr2-intelligent-task.csv")

df["device_type"] = df["device_type"].map({"desktop": 1, "mobile": 0})
X = df[["page_view", "ad_click", "avg_session_time", "bounce_rate", "device_type"]]
y = df["purchase"]

sns.pairplot(df, hue="purchase", vars=X.columns, palette="Set2")
plt.suptitle("Візуалізація поведінкових метрик", y=1.02)
plt.tight_layout()
plt.savefig("results/sr2-intelligent-task/pairplot.png")

lda = LinearDiscriminantAnalysis()
qda = QuadraticDiscriminantAnalysis(reg_param=0.1)

lda.fit(X, y)
qda.fit(X, y)

y_pred_lda = lda.predict(X)
y_pred_qda = qda.predict(X)

print("LDA Accuracy:", accuracy_score(y, y_pred_lda))
print("QDA Accuracy:", accuracy_score(y, y_pred_qda))

print("LDA Confusion Matrix:\n", confusion_matrix(y, y_pred_lda))
print("QDA Confusion Matrix:\n", confusion_matrix(y, y_pred_qda))

with open("results/sr2-intelligent-task/results.txt", "w") as f:
    f.write(f"LDA Accuracy: {accuracy_score(y, y_pred_lda):.2f}\n")
    f.write(f"QDA Accuracy: {accuracy_score(y, y_pred_qda):.2f}\n")
    f.write("LDA Confusion Matrix:\n")
    f.write(str(confusion_matrix(y, y_pred_lda)) + "\n")
    f.write("QDA Confusion Matrix:\n")
    f.write(str(confusion_matrix(y, y_pred_qda)) + "\n")

def simulate_action(df, action):
    df_copy = df.copy()
    if action == "increase_ad_budget":
        df_copy["ad_click"] += 2
    elif action == "optimize_landing_page":
        df_copy["bounce_rate"] = df_copy["bounce_rate"].apply(lambda x: max(x - 10, 0))
    elif action == "personalize_content":
        df_copy["avg_session_time"] += 30
    elif action == "add_product_reviews":
        df_copy["page_view"] += 5

    df_copy["device_type"] = df_copy["device_type"].map({"desktop": 1, "mobile": 0})

    if df_copy.isnull().values.any():
        df_copy = df_copy.fillna(0)

    X_sim = df_copy[["page_view", "ad_click", "avg_session_time", "bounce_rate", "device_type"]]
    y_sim = lda.predict(X_sim)
    return sum(y_sim)

def conversion_rate_after_action(action):
    predicted = simulate_action(df, action)
    rate = predicted / len(df)
    print(f"Прогнозована конверсія після '{action}': {rate:.2%}")
    return rate

with open("results/sr2-intelligent-task/report.md", "a", encoding="utf-8") as f:
    f.write(f"\n## Результати класифікації — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"- Модель LDA: точність {accuracy_score(y, y_pred_lda):.2f}\n")
    f.write(f"- Модель QDA: точність {accuracy_score(y, y_pred_qda):.2f} (з регуляризацією)\n")
    f.write("- Матриця помилок LDA:\n")
    f.write(str(confusion_matrix(y, y_pred_lda)) + "\n")
    f.write("- Матриця помилок QDA:\n")
    f.write(str(confusion_matrix(y, y_pred_qda)) + "\n")
    f.write("- Візуалізація метрик: ![](pairplot.png)\n")

    f.write("\n## Сценарне моделювання\n")
    for action in ["increase_ad_budget", "optimize_landing_page", "personalize_content", "add_product_reviews"]:
        rate = conversion_rate_after_action(action)
        f.write(f"- '{action}': прогнозована конверсія {rate:.2%}\n")