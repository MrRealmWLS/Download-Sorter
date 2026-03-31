# Download Sorter

A Python script that automatically organizes your Downloads folder by sorting files into categorized folders based on their file types.

## Features

- **Automatic File Sorting**: Organizes files in your Downloads folder into categorized subfolders
- **Multiple File Types Supported**: Images, Videos, Documents, Archives, Programs, Music, and Others
- **Duplicate Handling**: Automatically renames duplicate files to prevent overwriting
- **Folder Organization**: Moves existing folders into a dedicated "Folders" directory
- **Asynchronous Processing**: Fast processing with concurrent file operations
- **Dry Run Mode**: Test the organization without actually moving files

## Supported File Types

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`
- **Videos**: `.mp4`, `.mkv`, `.mov`, `.avi`
- **Documents**: `.pdf`, `.docx`, `.doc`, `.txt`, `.pptx`, `.xlsx`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Programs**: `.exe`, `.msi`
- **Music**: `.mp3`, `.wav`, `.ogg`

## Installation

1. Clone or download this repository to your local machine
2. Ensure you have Python installed (3.7 or higher)

## Usage

Simply run the script:

```bash
python tool.py
```

The script will automatically scan your Downloads folder and organize the files into appropriate subfolders.

## Configuration

The script includes several configurable options:

- `DRY_RUN`: Set to `True` to preview what would be moved without actually moving files
- `CONCURRENT_FILES`: Number of concurrent file operations (default: 150)
- `DOWNLOADS_PATH`: Path to the Downloads folder (defaults to user's Downloads folder)

## How It Works

1. The script scans all files in your Downloads folder
2. Based on file extensions, it determines the appropriate category
3. Files are moved to corresponding subfolders (Images, Videos, Documents, etc.)
4. Existing folders are moved to a "Folders" subdirectory
5. If a file with the same name already exists in the destination, it's renamed to avoid conflicts

## Safety Features

- Creates destination folders automatically if they don't exist
- Handles duplicate filenames by adding counters (e.g., `file(1).txt`)
- Maintains original file permissions during moves
- Includes safeguards against moving system or hidden folders

## License

This project is open source and available under the MIT License.

**Created by RealmWLS**
