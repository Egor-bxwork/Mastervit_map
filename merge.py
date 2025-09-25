import os
import json

INPUT_DIR = "merge"
OUTPUT_FILE = "full.json"

def merge_json_files(input_dir, output_file):
    merged = {
        "type": "FeatureCollection",
        "features": []
    }

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, "r", encoding="utf-8-sig") as f:  # <-- изменение здесь
                data = json.load(f)
                if "features" in data:
                    merged["features"].extend(data["features"])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=4)

    print(f"Объединенный файл сохранен в {output_file}")

if __name__ == "__main__":
    merge_json_files(INPUT_DIR, OUTPUT_FILE)
