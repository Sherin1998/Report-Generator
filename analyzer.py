import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd


CARDINALITY_THRESHOLD = 15


def generate_charts(df):

    os.makedirs("output", exist_ok=True)
    generated = []

    df.columns = df.columns.str.strip()

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # 🔥 Filter high-cardinality categorical columns
    filtered_categorical = [
        col for col in categorical_cols
        if df[col].nunique() <= CARDINALITY_THRESHOLD
    ]

    columns = numeric_cols + filtered_categorical

    print("Using columns for plotting:", columns)

    for i in range(len(columns)):
        col1 = columns[i]

        for j in range(i + 1, len(columns)):
            col2 = columns[j]

            plt.figure(figsize=(8, 5))

            try:

                # ===============================
                # 1️⃣ NUMERIC vs NUMERIC → SCATTER
                # ===============================
                if col1 in numeric_cols and col2 in numeric_cols:
                    sns.scatterplot(data=df, x=col1, y=col2)
                    chart_type = "scatter"

                # ===============================
                # 2️⃣ CATEGORICAL vs CATEGORICAL → BAR
                # ===============================
                elif col1 in filtered_categorical and col2 in filtered_categorical:
                    cross_tab = pd.crosstab(df[col1], df[col2])
                    cross_tab.plot(kind="bar", stacked=True)
                    chart_type = "bar"

                # ===============================
                # 3️⃣ NUMERIC + CATEGORICAL → PIE
                # ===============================
                elif (col1 in numeric_cols and col2 in filtered_categorical) or \
                     (col2 in numeric_cols and col1 in filtered_categorical):

                    cat_col = col1 if col1 in filtered_categorical else col2
                    counts = df[cat_col].value_counts()

                    counts.plot(kind="pie", autopct='%1.1f%%')
                    plt.ylabel("")
                    chart_type = "pie"

                else:
                    plt.close()
                    continue

                title = f"{col1} vs {col2}"
                plt.title(title)
                plt.xticks(rotation=45)
                plt.tight_layout()

                file_path = f"output/{col1}_vs_{col2}.png"
                file_path = file_path.replace(" ", "_")

                plt.savefig(file_path)
                plt.close()

                generated.append({
                    "title": title,
                    "chart_type": chart_type,
                    "columns": [col1, col2],
                    "path": file_path
                })

            except Exception as e:
                print(f"Skipping {col1} vs {col2}: {e}")
                plt.close()

    return generated
