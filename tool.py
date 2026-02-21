import os
import shutil
import asyncio

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
DRY_RUN = False
CONCURRENT_FILES = 150

FILE_TYPES = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".webp": "Images", ".svg": "Images",
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".avi": "Videos",
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "Documents", ".pptx": "Documents", ".xlsx": "Documents",
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".exe": "Programs", ".msi": "Programs",
    ".mp3": "Music", ".wav": "Music", ".ogg": "Music"
}

PREDEFINED_FOLDERS = set(FILE_TYPES.values())
semaphore = asyncio.Semaphore(CONCURRENT_FILES)


async def move_file(file_path, target_folder):
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
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.move, file_path, target_path)
        print(f"Moved: {fn} > {target_folder}")


async def process_file(fn):
    async with semaphore:
        path = os.path.join(DOWNLOADS_PATH, fn)
        if not os.path.isfile(path):
            return
        folder = FILE_TYPES.get(os.path.splitext(fn)[1].lower(), "Others")
        await move_file(path, folder)


async def move_all_folders():
    for entry in os.listdir(DOWNLOADS_PATH):
        full_path = os.path.join(DOWNLOADS_PATH, entry)
        if os.path.isdir(full_path) and entry not in PREDEFINED_FOLDERS and entry != "Folders":
            await move_file(full_path, "Folders")


async def organize_downloads():
    if not os.path.exists(DOWNLOADS_PATH):
        print("Downloads folder not found!")
        return
    files = [f for f in os.listdir(DOWNLOADS_PATH) if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))]
    await asyncio.gather(*(process_file(f) for f in files))
    await move_all_folders()
    print("Downloads organized successfully!")


if __name__ == "__main__":
    asyncio.run(organize_downloads())