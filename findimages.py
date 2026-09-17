import os
import shutil
from pathlib import Path
import sys

def find_and_move_images(source_dir):
    """
    Find all image files in source_dir (including in subdirectories)
    and move them to the source_dir.
    
    Args:
        source_dir: Path to the source directory.
    """
    # Common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
    
    # Convert to Path object
    source_path = Path(source_dir)
    
    # Ensure source directory exists
    if not source_path.is_dir():
        print(f"Error: {source_dir} is not a valid directory")
        return
    
    # Find all image files in all subdirectories
    moved_count = 0
    for root, _, files in os.walk(source_dir):
        # Skip the source directory itself
        if root == source_dir:
            continue
        
        for file in files:
            file_path = Path(root) / file
            file_ext = file_path.suffix.lower()
            
            # Check if it's an image file
            if file_ext in image_extensions:
                dest_path = source_path / file
                
                # Handle duplicate filenames
                if dest_path.exists():
                    base_name = file_path.stem
                    ext = file_path.suffix
                    counter = 1
                    while dest_path.exists():
                        new_name = f"{base_name}_{counter}{ext}"
                        dest_path = source_path / new_name
                        counter += 1
                
                # Move the file
                try:
                    shutil.move(str(file_path), str(dest_path))
                    moved_count += 1
                    print(f"Moved: {file_path} -> {dest_path}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
    
    print(f"\nTotal images moved: {moved_count}")

if __name__ == "__main__":
    folder_path = r"C:\Users\ycham\Downloads\images"
    
    find_and_move_images(folder_path)