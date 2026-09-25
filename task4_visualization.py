# TrendPulse — Task 4: create charts from the analysed data.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = Path("data") / "trends_analysed.csv"
OUTPUT_FOLDER = Path("outputs")

def shorten_title(title):
    """Shorten long story titles so they fit clearly on chart labels."""
    if len(title) > 50:
        return title[:47] + "..."

    return title

    # Create the outputs folder if it doesn't exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Load data from Task 3
df = pd.read_csv(INPUT_FILE)


# ----------------------------------------------------
# Task 2: Chart 1 — Top 10 Stories by Score
# ----------------------------------------------------
def create_chart1(df):
    # Sort top 10 stories by score
    top_10 = df.sort_values(by="score", ascending=False).head(10)
    
    # Apply title shortening
    titles = [shorten_title(title) for title in top_10["title"]]
    scores = top_10["score"]
    
    plt.figure(figsize=(10, 6))
    plt.barh(titles[::-1], scores[::-1], color="#2b5c8f")
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.tight_layout()
    
    # Save chart before showing
    plt.savefig(OUTPUT_FOLDER / "chart1_top_stories.png", dpi=300)
    plt.close()


# ----------------------------------------------------
# Task 3: Chart 2 — Stories per Category
# ----------------------------------------------------
def create_chart2(df):
    category_counts = df["category"].value_counts()
    
    plt.figure(figsize=(8, 5))
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#e67e22"]
    
    plt.bar(
        category_counts.index, 
        category_counts.values, 
        color=colors[:len(category_counts)]
    )
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    
    plt.savefig(OUTPUT_FOLDER / "chart2_categories.png", dpi=300)
    plt.close()


# ----------------------------------------------------
# Task 4: Chart 3 — Score vs Comments
# ----------------------------------------------------
def create_chart3(df):
    plt.figure(figsize=(8, 6))
    
    popular_mask = df["is_popular"] == True
    non_popular_mask = df["is_popular"] == False
    
    # Scatter non-popular
    plt.scatter(
        df.loc[non_popular_mask, "score"],
        df.loc[non_popular_mask, "num_comments"],
        color="#95a5a6",
        alpha=0.6,
        label="Non-Popular"
    )
    
    # Scatter popular
    plt.scatter(
        df.loc[popular_mask, "score"],
        df.loc[popular_mask, "num_comments"],
        color="#e74c3c",
        alpha=0.8,
        label="Popular"
    )
    
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments (Popularity)")
    plt.legend(title="Status")
    plt.tight_layout()
    
    plt.savefig(OUTPUT_FOLDER / "chart3_scatter.png", dpi=300)
    plt.close()


# ----------------------------------------------------
# Bonus: Combined Dashboard
# ----------------------------------------------------
def create_dashboard(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold")
    
    # 1. Top Stories
    top_10 = df.sort_values(by="score", ascending=False).head(10)
    titles = [shorten_title(t) for t in top_10["title"]]
    axes[0, 0].barh(titles[::-1], top_10["score"][::-1], color="#2b5c8f")
    axes[0, 0].set_xlabel("Score")
    axes[0, 0].set_ylabel("Story Title")
    axes[0, 0].set_title("Top 10 Stories by Score")
    
    # 2. Categories
    category_counts = df["category"].value_counts()
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#e67e22"]
    axes[0, 1].bar(
        category_counts.index, 
        category_counts.values, 
        color=colors[:len(category_counts)]
    )
    axes[0, 1].set_xlabel("Category")
    axes[0, 1].set_ylabel("Number of Stories")
    axes[0, 1].set_title("Stories per Category")
    axes[0, 1].tick_params(axis="x", rotation=30)
    
    # 3. Score vs Comments
    popular_mask = df["is_popular"] == True
    non_popular_mask = df["is_popular"] == False
    
    axes[1, 0].scatter(
        df.loc[non_popular_mask, "score"], 
        df.loc[non_popular_mask, "num_comments"], 
        color="#95a5a6", alpha=0.6, label="Non-Popular"
    )
    axes[1, 0].scatter(
        df.loc[popular_mask, "score"], 
        df.loc[popular_mask, "num_comments"], 
        color="#e74c3c", alpha=0.8, label="Popular"
    )
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Number of Comments")
    axes[1, 0].set_title("Score vs Comments")
    axes[1, 0].legend()
    
    # Hide empty 4th subplot
    axes[1, 1].axis("off")
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(OUTPUT_FOLDER / "dashboard.png", dpi=300)
    plt.close()


# Execute functions
if __name__ == "__main__":
    create_chart1(df)
    create_chart2(df)
    create_chart3(df)
    create_dashboard(df)
    print("All charts and dashboard generated successfully in 'outputs/'.")