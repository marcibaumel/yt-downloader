# Homemade YouTube Video Downloader

A simple Python application to download YouTube videos.

## Features
- Download YouTube videos in various resolutions
- Supports audio-only downloads
- Easy-to-use command-line interface

## Manual

### Install

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the program from the console:
```bash
python main.py
```

### Generate Executable

If you want to create a standalone executable:
```bash
pyinstaller --onefile main.py
```
This will generate an executable in the `dist/` directory.

## Requirements
Ensure you have the following installed:
- Python 3.x
- `pip` (Python package manager)

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

## Disclaimer
This tool is intended for personal use only. Downloading videos from YouTube may violate YouTube's terms of service. Use responsibly.