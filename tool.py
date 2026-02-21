import os
import shutil
import hashlib

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
DRY_RUN = True

FILE_TYPES = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".webp": "Images", ".svg": "Images",
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".avi": "Videos",
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "Documents", ".pptx": "Documents", ".xlsx": "Documents",
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".exe": "Programs", ".msi": "Programs",
    ".mp3": "Music", ".wav": "Music", ".ogg": "Music"
}

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def move_file(file_path, target_folder):
    fn = os.path.basename(file_path)
    folder_path = os.path.join(DOWNLOADS_PATH, target_folder)
    os.makedirs(folder_path, exist_ok=True)
    target_path = os.path.join(folder_path, fn)
    if os.path.exists(target_path):
        base, ext = os.path.splitext(fn)
        counter = 1
        while os.path.exists(os.path.join(folder_path, f"{base}({counter}){ext}")):
            counter += 1
        target_path = os.path.join(folder_path, f"{base}({counter}){ext}")
    if DRY_RUN:
        print(f"[DRY RUN] Would move: {fn} > {target_folder}")
    else:
        shutil.move(file_path, target_path)
        print(f"Moved: {fn} > {target_folder}")

def organize_downloads():
    if not os.path.exists(DOWNLOADS_PATH):
        print("Downloads folder not found!")
        return
    seen_hashes = set()
    files = [f for f in os.listdir(DOWNLOADS_PATH) if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))]
    for fn in files:
        path = os.path.join(DOWNLOADS_PATH, fn)
        h = file_hash(path)
        if h in seen_hashes:
            move_file(path, "Duplicates")
            continue
        seen_hashes.add(h)
        folder = FILE_TYPES.get(os.path.splitext(fn)[1].lower(), "Others")
        move_file(path, folder)
    print("Downloads organized successfully!")

if __name__ == "__main__":
    organize_downloads()