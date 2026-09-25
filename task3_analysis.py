# TrendPulse — Task 3: analyse the cleaned data with Pandas and NumPy.

from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILE = Path("data") / "trends_clean.csv"
OUTPUT_FILE = Path("data") / "trends_analysed.csv"

def main():
    """Load cleaned data, calculate statistics, and save analysed data."""
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} was not found. Run Task 2 first.")
        return

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded data: {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head())

    average_score = df["score"].mean()
    average_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {average_score:.2f}")
    print(f"Average comments: {average_comments:.2f}")

    # Convert scores to a NumPy array for the required NumPy calculations.
    scores = df["score"].to_numpy()

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Std deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # Find the category containing the most stories.
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_category_count = category_counts.max()

    print(
        f"\nMost stories in: {top_category} "
        f"({top_category_count} stories)"
    )

    # Find the story with the largest number of comments.
    most_commented = df.loc[df["num_comments"].idxmax()]

    print(
        f'\nMost commented story: "{most_commented["title"]}" '
        f'— {most_commented["num_comments"]} comments'
    )

    # Add the two required columns for Task 4.
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    df["is_popular"] = df["score"] > average_score

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()