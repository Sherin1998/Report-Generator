import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_charts(df, plan):

    os.makedirs("output", exist_ok=True)

    generated = []

    for chart in plan["charts"]:

        chart_type = chart["chart_type"]
        columns = chart["columns"]
        title = chart["title"]

        plt.figure()

        if chart_type == "line":
            df[columns].plot()

        elif chart_type == "bar":
            df[columns[0]].value_counts().plot(kind="bar")

        elif chart_type == "histogram":
            df[columns[0]].plot(kind="hist", bins=20)

        elif chart_type == "scatter" and len(columns) >= 2:
            plt.scatter(df[columns[0]], df[columns[1]])
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])

        elif chart_type == "box":
            df[columns].plot(kind="box")

        elif chart_type == "heatmap":
            corr = df.select_dtypes(include="number").corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0)

        plt.title(title)

        file_path = f"output/{title.replace(' ', '_')}.png"
        plt.savefig(file_path)
        plt.close()

        generated.append({
            "title": title,
            "path": file_path,
            "columns": columns
        })

    return generated