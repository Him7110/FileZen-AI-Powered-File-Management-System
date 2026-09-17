import sys
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget, QListWidget, 
                             QLabel, QFileDialog, QComboBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from indexer import process_file, index_folder


class ModernSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neural Desktop Search")
        self.setGeometry(100, 100, 900, 600)
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # --- Top Control Panel ---
        top_layout = QHBoxLayout()
        
        self.btn_index = QPushButton("📂 Index New Folder")
        self.btn_index.clicked.connect(self.select_folder)
        self.btn_index.setStyleSheet("padding: 10px; background-color: #2b2b2b; color: white;")
        
        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("Tag/Class (e.g., 'Work', 'Vacation')")
        
        top_layout.addWidget(self.btn_index)
        top_layout.addWidget(self.input_category)
        layout.addLayout(top_layout)

        # --- Search Bar ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Describe what you are looking for (e.g., 'invoice from march', 'sunset at beach', 'audio about meeting')...")
        self.search_bar.setStyleSheet("font-size: 16px; padding: 10px;")
        self.search_bar.returnPressed.connect(self.perform_search)
        layout.addWidget(self.search_bar)

        # --- Results Area ---
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)
        
        # Preview Area (Simple image viewer label)
        self.preview_label = QLabel("Preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid #ccc; min-height: 200px;")
        layout.addWidget(self.preview_label)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Index")
        category = self.input_category.text() or "General"
        if folder:
            # Run indexing in a separate thread to not freeze UI
            threading.Thread(target=index_folder, args=(folder, category)).start()
            self.results_list.addItem(f"Started indexing {folder} as '{category}'...")

    def perform_search(self):
        query = self.search_bar.text()
        if not query: return
        
        self.results_list.clear()
        
        # This is where the magic happens: Multimodal Search
        # We query using text, but it matches images AND text documents
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=['metadatas', 'documents', 'uris']
        )

        ids = results['ids'][0]
        metas = results['metadatas'][0]
        
        for i, file_id in enumerate(ids):
            meta = metas[i]
            display_text = f"[{meta['category']}] {meta['filename']} \nPath: {meta['path']}"
            self.results_list.addItem(display_text)

    # Optional: Add click handler to results_list to show preview in preview_label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernSearchApp()
    window.show()
    sys.exit(app.exec())