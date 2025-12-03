import json
from collections import Counter, defaultdict
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "data loot.cdb"

def load_sheets(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sheets", [])

def top_level_counts(sheets):
    counter = Counter()
    for sheet in sheets:
        name = sheet.get("name", "")
        top = name.split("@", 1)[0]
        counter[top] += 1
    return counter

def nested_counts(sheets):
    nested = defaultdict(Counter)
    for sheet in sheets:
        name = sheet.get("name", "")
        parts = name.split("@")
        if len(parts) >= 2:
            nested[parts[0]][parts[1]] += 1
    return nested

def print_summary(sheets):
    print(f"Total sheets: {len(sheets)}")
    top_counts = top_level_counts(sheets)
    print("\nTop-level groups (count):")
    for name, count in top_counts.most_common():
        print(f"  {name}: {count}")

    nested = nested_counts(sheets)
    print("\nSecond-level groups (count per top-level):")
    for top, counter in sorted(nested.items()):
        most_common = counter.most_common(5)
        formatted = ", ".join(f"{name} ({count})" for name, count in most_common)
        print(f"  {top}: {formatted}")

    depth_counter = Counter(len(sheet.get("name", "").split("@")) for sheet in sheets)
    print("\nSheet name depth distribution (number of '@' + 1):")
    for depth, count in sorted(depth_counter.items()):
        print(f"  depth {depth}: {count}")

def main():
    sheets = load_sheets(FILE_PATH)
    if not sheets:
        print("No sheets found.")
        return
    print_summary(sheets)

if __name__ == "__main__":
    main()
