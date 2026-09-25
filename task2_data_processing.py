# TrendPulse — Task 2: clean the collected data and save it as CSV.

from pathlib import Path

import pandas as pd


DATA_FOLDER = Path("data")
OUTPUT_FILE = DATA_FOLDER / "trends_clean.csv"

def find_latest_json_file():
    """Find the newest JSON file created by Task 1."""
    json_files = sorted(DATA_FOLDER.glob("trends_*.json"))

    if not json_files:
        print("Error: no trends JSON file was found in the data folder.")
        return None

    return json_files[-1]

def main():
    """Load Task 1 data, clean it, and save a CSV file."""
    json_file = find_latest_json_file()

    if json_file is None:
        return

    try:
        df = pd.read_json(json_file)
    except ValueError as error:
        print(f"Could not load JSON file: {error}")
        return

    print(f"Loaded {len(df)} stories from {json_file}")

    # Remove duplicate stories using their unique Hacker News post ID.
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Strip whitespace before checking for missing title values.
    df["title"] = df["title"].astype("string").str.strip()

    # Convert score and comment columns to numbers.
    # Invalid score values become missing and are removed below.
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(
        df["num_comments"],
        errors="coerce"
    ).fillna(0)

    # Remove rows missing essential data.
    df = df.dropna(subset=["post_id", "title", "score"]).copy()
    df = df[df["title"] != ""].copy()
    print(f"After removing nulls: {len(df)}")

    # Make score and comment counts integer values.
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Keep only stories with a score of at least 5.
    df = df[df["score"] >= 5].copy()
    print(f"After removing low scores: {len(df)}")

    # Save the cleaned data without the Pandas index column.
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_FILE}")

    print("\nStories per category:")
    category_counts = df["category"].value_counts()

    for category, count in category_counts.items():
        print(f"  {category:<15} {count}")


if __name__ == "__main__":
    main()