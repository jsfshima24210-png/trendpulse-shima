# TrendPulse — Task 1: collect and categorise Hacker News stories.

import json
import time
from datetime import datetime
from pathlib import Path

import requests


TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election",
        "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}

def get_top_story_ids():
    """Fetch the first 500 trending Hacker News story IDs."""
    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()

        story_ids = response.json()

        if not isinstance(story_ids, list):
            print("Error: Hacker News did not return a list of story IDs.")
            return []

        return story_ids[:500]

    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch top stories: {error}")
        return []

def get_story(story_id):
    """Fetch the details of one Hacker News story."""
    try:
        story_url = ITEM_URL.format(story_id)

        response = requests.get(
            story_url,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()

        return response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch story {story_id}: {error}")
        return None

def title_matches(title, keywords):
    """Return True if a title contains any keyword."""
    title_lower = title.lower()

    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True

    return False

def create_record(story, story_id, category, collected_at):
    """Create one JSON-ready record with all required fields."""
    return {
        "post_id": story.get("id", story_id),
        "title": story.get("title", ""),
        "category": category,
        "score": story.get("score") or 0,
        "num_comments": story.get("descendants") or 0,
        "author": story.get("by") or "unknown",
        "collected_at": collected_at
    }

def main():
    """Collect stories, save them to JSON, and print the result."""
    top_story_ids = get_top_story_ids()

    if not top_story_ids:
        print("No stories collected because top story IDs could not be loaded.")
        return

    all_stories = []
   
    story_cache = {}
    collected_at = datetime.now().isoformat(timespec="seconds")
    category_items = list(CATEGORIES.items())

    for category_index, (category, keywords) in enumerate(category_items):
        category_count = 0
        print(f"Collecting {category} stories...")

        for story_id in top_story_ids:
            if category_count >= 25:
                break

            


            if story_id not in story_cache:
                story_cache[story_id] = get_story(story_id)

            story = story_cache[story_id]

            if not isinstance(story, dict):
                continue

            title = story.get("title", "")

            if not isinstance(title, str) or not title.strip():
                continue

            if title_matches(title, keywords):
                record = create_record(
                    story,
                    story_id,
                    category,
                    collected_at
                )

                all_stories.append(record)
                
                category_count += 1

        print(f"Collected {category_count} {category} stories.")

        if category_index < len(category_items) - 1:
            time.sleep(2)

    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    date_text = datetime.now().strftime("%Y%m%d")
    output_file = data_folder / f"trends_{date_text}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_stories, file, indent=4, ensure_ascii=False)

    print(f"Collected {len(all_stories)} stories. Saved to {output_file}")


if __name__ == "__main__":
    main()

