import os
import shutil
import hashlib
import re
from datetime import datetime

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi"],
    "Music": [".mp3", ".wav", ".ogg"],
}

DRY_RUN = True


def file_hash(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def move_file(file_path, target_folder):
    filename = os.path.basename(file_path)
    folder_path = os.path.join(DOWNLOADS_PATH, target_folder)
    os.makedirs(folder_path, exist_ok=True)
    target_path = os.path.join(folder_path, filename)

    if os.path.exists(target_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(folder_path, f"{base}({counter}){ext}")):
            counter += 1
        target_path = os.path.join(folder_path, f"{base}({counter}){ext}")

    if DRY_RUN:
        print(f"[DRY RUN] Would move: {filename} > {target_folder}")
    else:
        shutil.move(file_path, target_path)
        print(f"Moved: {filename} > {target_folder}")

def organize_downloads():
    if not os.path.exists(DOWNLOADS_PATH):
        print("Downloads folder not found!")
        return

    seen_hashes = set()
    for filename in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, filename)

        if os.path.isdir(file_path):
            continue
        file_h = file_hash(file_path)
        if file_h in seen_hashes:
            move_file(file_path, "Duplicates")
            continue
        seen_hashes.add(file_h)

        file_ext = os.path.splitext(filename)[1].lower()
        matched = False
        for folder_name, extensions in FILE_TYPES.items():
            if file_ext in extensions:
                move_file(file_path, folder_name)
                matched = True
                break
        if matched:
            continue

        move_file(file_path, "Others")

    print("Downloads organized successfully!")


if __name__ == "__main__":
    organize_downloads()