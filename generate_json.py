import os
import json
import re

PROJECTS_DIR = "projects"
OUTPUT_FILE = "projects.json"
BASE_URL = "https://junothecat.github.io/housing-catalogue"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)  # remove punctuation
    text = re.sub(r'[\s-]+', '-', text)       # replace spaces/hyphens with single hyphen
    return text.strip('-')

def read_project_data(project_path, folder_name):
    info_path = os.path.join(project_path, "info.txt")
    image_path = os.path.join(project_path, "image.jpg")

    if not os.path.exists(info_path) or not os.path.exists(image_path):
        return None

    project_data = {}
    current_key = None
    multiline_buffer = []

    with open(info_path, 'r', encoding='utf-8') as f:
        for line in f:
            # New key:value pair
            if ':' in line and not line.startswith(' ') and not line.strip().startswith('\t') and line.index(':') < 30:
                if current_key and multiline_buffer:
                    project_data[current_key] = ''.join(multiline_buffer).strip('\n')
                    multiline_buffer = []

                key, value = line.strip().split(':', 1)
                key = key.strip()
                value = value.strip()

                if value:
                    project_data[key] = value
                    current_key = None
                else:
                    current_key = key
                    multiline_buffer = []
            elif current_key:
                multiline_buffer.append(line)

    if current_key and multiline_buffer:
        project_data[current_key] = ''.join(multiline_buffer).strip('\n')

    if 'title' not in project_data:
        return None

    project_data["image"] = f"{BASE_URL}/{PROJECTS_DIR}/{folder_name}/image.jpg"
    project_data["slug"] = slugify(project_data["title"])

    return project_data

def build_json():
    projects = []
    for folder in os.listdir(PROJECTS_DIR):
        path = os.path.join(PROJECTS_DIR, folder)
        if os.path.isdir(path):
            data = read_project_data(path, folder)
            if data:
                projects.append(data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    print(f"✅ Compiled {len(projects)} projects into {OUTPUT_FILE}")

if __name__ == "__main__":
    build_json()
