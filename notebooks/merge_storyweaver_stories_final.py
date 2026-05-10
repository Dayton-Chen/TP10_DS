#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path


CATEGORY_NAMES = {
    "ANIMALS": "Animal World",
    "NATURE": "Real World & Discovery",
    "DAILY_LIFE": "Story Adventures",
}


SW_THEME_TO_CATEGORY = {
    "Animal Stories": CATEGORY_NAMES["ANIMALS"],
    "STEM": CATEGORY_NAMES["NATURE"],
    "Non-fiction": CATEGORY_NAMES["NATURE"],
    "History": CATEGORY_NAMES["NATURE"],
    "Biographies": CATEGORY_NAMES["NATURE"],
    "Family & Friends": CATEGORY_NAMES["DAILY_LIFE"],
    "Growing Up": CATEGORY_NAMES["DAILY_LIFE"],
    "Funny": CATEGORY_NAMES["DAILY_LIFE"],
    "Adventure & Mystery": CATEGORY_NAMES["DAILY_LIFE"],
    "Fantasy": CATEGORY_NAMES["DAILY_LIFE"],
    "Classics": CATEGORY_NAMES["DAILY_LIFE"],
    "Scary": CATEGORY_NAMES["DAILY_LIFE"],
}

EXCLUDED_SW_THEMES = {
    "Award Winning": "Not a content theme",
    "Read-Aloud Stories": "Reading format, not content type",
    "Activity Books": "Activity format, content may vary",
}


def unified_level_from_word_count(word_count):
    if word_count <= 250:
        return "level_1"
    if word_count <= 600:
        return "level_2"
    return "level_3"


def load_json(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def init_result():
    return {
        CATEGORY_NAMES["ANIMALS"]: {"level_1": [], "level_2": [], "level_3": []},
        CATEGORY_NAMES["NATURE"]: {"level_1": [], "level_2": [], "level_3": []},
        CATEGORY_NAMES["DAILY_LIFE"]: {"level_1": [], "level_2": [], "level_3": []},
    }


def merge_storyweaver(result, storyweaver):
    counts = Counter()
    for theme, levels in storyweaver.items():
        if theme in EXCLUDED_SW_THEMES:
            continue
        mapped_category = SW_THEME_TO_CATEGORY[theme]
        for level_key, items in levels.items():
            for item in items:
                record = {
                    "id": item["id"],
                    "title": item.get("title"),
                    "Text": item["Text"],
                    "word_count": item["word_count"],
                    "Source": item.get("Source", "StoryWeaver"),
                    "source_dataset": "storyweaver",
                    "source_url": item.get("source_url"),
                    "author": item.get("author"),
                    "illustrator": item.get("illustrator"),
                    "original_theme": theme,
                    "mapped_category": mapped_category,
                    "original_reading_level": item.get("reading_level"),
                    "unified_reading_level": level_key,
                }
                result[mapped_category][level_key].append(record)
                counts[(mapped_category, level_key)] += 1
    return counts


def merge_stories_final(result, stories_final):
    counts = Counter()
    for category, levels in stories_final.items():
        mapped_category = CATEGORY_NAMES[category]
        for original_level_key, items in levels.items():
            for item in items:
                unified_level = unified_level_from_word_count(item.get("word_count", 0))
                record = {
                    "id": item["id"],
                    "title": None,
                    "Text": item["Text"],
                    "word_count": item["word_count"],
                    "Source": item.get("Source"),
                    "source_dataset": "stories_final",
                    "source_url": None,
                    "author": None,
                    "illustrator": None,
                    "original_theme": category,
                    "mapped_category": mapped_category,
                    "original_reading_level": original_level_key,
                    "unified_reading_level": unified_level,
                    "dale_chall": item.get("dale_chall"),
                }
                result[mapped_category][unified_level].append(record)
                counts[(mapped_category, unified_level)] += 1
    return counts


def main():
    storyweaver = load_json("storyweaver_texts_cleaned.json")
    stories_final = load_json("stories_final.json")

    result = init_result()
    sw_counts = merge_storyweaver(result, storyweaver)
    sf_counts = merge_stories_final(result, stories_final)

    output_path = Path("merged_story_corpus_3class.json")
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "reading_level_rule": {
            "level_1": "0-250 words",
            "level_2": "251-600 words",
            "level_3": "601+ words",
            "note": "Used StoryWeaver-style word-count buckets; texts above 1500 words are also placed in level_3.",
        },
        "storyweaver_theme_mapping": SW_THEME_TO_CATEGORY,
        "excluded_storyweaver_themes": EXCLUDED_SW_THEMES,
        "storyweaver_counts_by_category_level": {
            f"{category}/{level}": count
            for (category, level), count in sorted(sw_counts.items())
        },
        "stories_final_counts_by_category_level": {
            f"{category}/{level}": count
            for (category, level), count in sorted(sf_counts.items())
        },
        "merged_counts_by_category_level": {
            f"{category}/{level}": len(items)
            for category, levels in result.items()
            for level, items in levels.items()
        },
        "merged_totals_by_category": {
            category: sum(len(items) for items in levels.values())
            for category, levels in result.items()
        },
        "total_records": sum(
            len(items)
            for levels in result.values()
            for items in levels.values()
        ),
    }

    summary_path = Path("merged_story_corpus_3class_summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"saved {output_path}")
    print(f"saved {summary_path}")
    print(json.dumps(summary["merged_totals_by_category"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
