# FileZen

FileZen is an AI-assisted desktop file organizer. It can sort files by extension or analyze their content with a trained image classifier and a sentence-embedding model. The project also contains an experimental semantic-search interface for indexing images, text, audio, and video.

## Features

- Organize files by AI-detected content or file extension.
- Copy files to a new location or move them in place.
- Place files in category folders or add the category to the filename.
- Classify images with the bundled MobileNetV2 model.
- Classify text from PDF, DOCX, TXT, and Markdown files using semantic similarity.
- Use optional OCR to classify text-heavy images.
- Search-index prototype support for images, text, audio, and video in `v2/`.

## Project Layout

```text
.
├── gui_app.py                 # Tkinter file-organizer desktop app
├── inference.py               # Image and text classification helpers
├── image_train.py             # Train a classifier from dataset/images/
├── findimages.py              # Flatten images from nested folders
├── models/
│   ├── image_classifier_model.h5
│   ├── class_labels.json
│   └── paraphrase-MiniLM-L6-v2/
├── dataset/images/            # Training images grouped by class
├── v2/app.py                  # Experimental PyQt semantic-search UI
└── v2/indexer.py              # ChromaDB indexing pipeline
```

## Requirements

- Python 3.9 or newer is recommended.
- TensorFlow may require a compatible Python version and platform-specific installation.
- The `models/` directory must remain in the repository because the classifier and embedding model load from it.
- `easyocr` is optional. Without it, the organizer still works but cannot read text embedded in images.

## Installation

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

To enable OCR in the Tkinter app, install the optional dependency:

```bash
python -m pip install easyocr
```

## Run the File Organizer

Run this command from the repository root so the bundled model paths resolve correctly:

```bash
python gui_app.py
```

In the application:

1. Select a source folder and a destination folder.
2. Choose **Content Analysis (AI)** or **File Extension**.
3. Choose **Separate by Folders** or add the category to each filename.
4. Choose **Copy Files** first if you want to preserve the originals. Use **Move Files** only after checking the selected paths.
5. Select **Organize Files**.

Content analysis currently supports:

| File types                       | Processing                                                |
| -------------------------------- | --------------------------------------------------------- |
| `.png`, `.jpg`, `.jpeg`, `.webp` | Image classifier, with optional OCR for text-heavy images |
| `.pdf`, `.docx`, `.txt`, `.md`   | Text extraction and semantic classification               |
| `.csv`, `.xlsx`                  | Datasheets category                                       |
| `.mp4`, `.mkv`, `.webm`          | Videos category                                           |
| `.mp3`, `.wav`                   | Audios category                                           |
| `.zip`, `.rar`, `.7z`            | Archives category                                         |

## Train the Image Model

Training images should be arranged in one folder per class under `dataset/images/`:

```text
dataset/images/
├── Documents/
├── Nature/
├── Pets_animals/
└── ...
```

Run training from the repository root:

```bash
python image_train.py
```

The script writes the trained weights to `models/image_classifier_model.h5` and the class names to `models/class_labels.json`. Review the dataset path in `image_train.py` before training because it currently contains a machine-specific path.

## Experimental Semantic Search (`v2`)

The `v2/` directory contains a separate PyQt6 and ChromaDB prototype. Its indexer can embed image content, text files, audio transcriptions, and video thumbnails. It creates a local `my_local_search_db/` directory and may download model assets on first use.

This prototype is under active development and is not yet as reliable as the Tkinter organizer. Run it from the repository root with:

```bash
python v2/app.py
```

The prototype may also require additional system support for Whisper, OpenCV, and ChromaDB beyond the packages listed in `requirements.txt`.

## Troubleshooting

- **Model file not found:** run commands from the repository root and confirm `models/image_classifier_model.h5` exists.
- **TensorFlow installation errors:** use a Python version supported by the TensorFlow release available for your operating system.
- **OCR is disabled:** install `easyocr`; the app will otherwise continue without OCR.
- **The app reports existing files:** existing destination files are skipped rather than overwritten.

## Known Limitations

- The organizer processes files directly in the selected source directory, not nested subdirectories.
- Classification categories are defined in code and are not yet configurable from the UI.
- The training script contains a hard-coded dataset path that must be changed on another machine.
- The `v2` search app is experimental and may require code changes before use.

## License

No license file is currently included in this repository.
