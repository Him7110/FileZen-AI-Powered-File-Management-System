import os
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import cv2
import whisper
import threading

# --- Configuration ---
DB_PATH = "./my_local_search_db"
client = chromadb.PersistentClient(path=DB_PATH)
image_loader = ImageLoader()
embedding_func = OpenCLIPEmbeddingFunction()

# Create a multimodal collection
collection = client.get_or_create_collection(
    name="desktop_files",
    embedding_function=embedding_func,
    data_loader=image_loader
)

# Load Whisper model for Audio (Load once)
print("Loading Audio Model...")
audio_model = whisper.load_model("base")

def process_file(file_path, category="Uncategorized"):
    """
    Decides how to process a file based on extension.
    """
    ext = file_path.split('.')[-1].lower()
    filename = os.path.basename(file_path)
    
    metadata = {"path": file_path, "filename": filename, "category": category}

    try:
        # 1. IMAGES
        if ext in ['png', 'jpg', 'jpeg', 'webp']:
            # ChromaDB handles image loading automatically via URIs if using OpenCLIP
            collection.add(
                ids=[file_path],
                uris=[file_path],
                metadatas=[metadata]
            )
            print(f"Indexed Image: {filename}")

        # 2. TEXT FILES (txt, md, py, etc.)
        elif ext in ['txt', 'md', 'py', 'csv']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
            
            # Chunking is recommended for large files, keeping it simple here
            collection.add(
                ids=[file_path],
                documents=[text_content],
                metadatas=[metadata]
            )
            print(f"Indexed Text: {filename}")

        # 3. AUDIO (mp3, wav)
        elif ext in ['mp3', 'wav', 'm4a']:
            # Transcribe audio to text, then embed the text
            result = audio_model.transcribe(file_path)
            transcription = result['text']
            
            collection.add(
                ids=[file_path],
                documents=[transcription], # We search the CONTENT of the audio
                metadatas=metadata
            )
            print(f"Indexed Audio: {filename}")

        # 4. VIDEO (mp4, mkv) - Advanced Strategy
        elif ext in ['mp4', 'mkv', 'avi']:
            # Strategy: Extract a thumbnail from the middle and index it as an image
            # AND transcribe the audio track.
            
            # A. Visual Indexing (Middle Frame)
            cap = cv2.VideoCapture(file_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
            ret, frame = cap.read()
            if ret:
                thumb_path = f"./temp_thumbs/{filename}.jpg"
                os.makedirs("./temp_thumbs", exist_ok=True)
                cv2.imwrite(thumb_path, frame)
                
                collection.add(
                    ids=[file_path + "_visual"],
                    uris=[thumb_path],
                    metadatas={**metadata, "type": "video_frame"}
                )
            cap.release()
            print(f"Indexed Video Visuals: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def index_folder(folder_path, category_tag):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            process_file(full_path, category_tag)