import os
import shutil

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi"],
    "Music": [".mp3", ".wav", ".ogg"],
}

def organize_downloads():
    if not os.path.exists(DOWNLOADS_PATH):
        print("Downloads folder not found!")
        return

    for filename in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, filename)

        if os.path.isdir(file_path):
            continue

        file_ext = os.path.splitext(filename)[1].lower()

        moved = False

        for folder_name, extensions in FILE_TYPES.items():
            if file_ext in extensions:
                folder_path = os.path.join(DOWNLOADS_PATH, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, filename))
                print(f"Moved: {filename} > {folder_name}")
                moved = True
                break

        if not moved:
            other_folder = os.path.join(DOWNLOADS_PATH, "Others")
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(other_folder, filename))
            print(f"Moved: {filename} > Others")

    print("Downloads organized successfully!")

if __name__ == "__main__":
    organize_downloads()