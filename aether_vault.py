#!/usr/bin/env python3
"""
AetherVault - Secure File Encryption & Steganography Tool
Copyright (c) 2024 - MIT License
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from crypto_manager import CryptoManager
from image_factory import ImageFactory


class ProcessingThread(QThread):
    """Background thread for encryption/decryption operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, mode, file_path, password, crypto_manager, img_factory):
        super().__init__()
        self.mode = mode
        self.file_path = file_path
        self.password = password
        self.crypto = crypto_manager
        self.img_factory = img_factory
        
    def run(self):
        try:
            if self.mode == "ENCRYPT":
                self._encrypt()
            else:
                self._decrypt()
            self.finished.emit(True, "Operation completed successfully")
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def _encrypt(self):
        self.progress.emit("Encrypting file...")
        encrypted_bytes = self.crypto.encrypt_data(self.file_path, self.password)
        
        self.progress.emit("Generating cover image...")
        cover_img = self.img_factory.generate_cover_image()
        
        self.progress.emit("Embedding encrypted data...")
        final_img = self.img_factory.embed_data(cover_img, encrypted_bytes)
        
        base_name = os.path.splitext(self.file_path)[0]
        out_path = f"{base_name}_VAULT.png"
        final_img.save(out_path)
        
    def _decrypt(self):
        self.progress.emit("Extracting encrypted data...")
        encrypted_bytes = self.img_factory.extract_data(self.file_path)
        
        self.progress.emit("Decrypting file...")
        plaintext, ext = self.crypto.decrypt_data(encrypted_bytes, self.password)
        
        base_name = self.file_path.replace("_VAULT", "").replace(".png", "")
        out_path = f"{base_name}_RECOVERED{ext}"
        
        with open(out_path, 'wb') as f:
            f.write(plaintext)


class AetherVaultApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.crypto = CryptoManager()
        self.img_factory = ImageFactory()
        self.processing_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("AetherVault - Secure File Encryption")
        self.setMinimumSize(900, 700)
        self.setAcceptDrops(True)
        
        self.setStyleSheet(self._get_stylesheet())
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("AETHER VAULT")
        header.setFont(QFont("Courier New", 28, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00ff41; padding: 20px;")
        main_layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Offline Encryption & Steganography System")
        subtitle.setFont(QFont("Consolas", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888; margin-bottom: 10px;")
        main_layout.addWidget(subtitle)
        
        # File list section
        list_label = QLabel("FILE QUEUE")
        list_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        list_label.setStyleSheet("color: #00ff41;")
        main_layout.addWidget(list_label)
        
        # Table widget for files
        self.file_table = QTableWidget(0, 4)
        self.file_table.setHorizontalHeaderLabels(["Filename", "Size", "Type", "Status"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.file_table.setMinimumHeight(250)
        self.file_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.file_table)
        
        # Action buttons for file list
        btn_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Add Files")
        self.btn_add.clicked.connect(self.add_files)
        self.btn_add.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_add)
        
        self.btn_clear = QPushButton("Clear List")
        self.btn_clear.clicked.connect(self.clear_list)
        self.btn_clear.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(btn_layout)
        
        # Password section
        pwd_label = QLabel("ENCRYPTION KEY")
        pwd_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        pwd_label.setStyleSheet("color: #00ff41; margin-top: 10px;")
        main_layout.addWidget(pwd_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter encryption password...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        main_layout.addWidget(self.password_input)
        
        # Info label
        info = QLabel("Maximum file size: ~2.5 MB | Drag and drop files or use Add Files button")
        info.setStyleSheet("color: #666; font-size: 10px; margin-top: 5px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(info)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #00ff41; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Process button
        self.btn_process = QPushButton("PROCESS FILES")
        self.btn_process.setMinimumHeight(60)
        self.btn_process.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.btn_process.clicked.connect(self.process_files)
        main_layout.addWidget(self.btn_process)
        
        central.setLayout(main_layout)
    
    def _get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #0a0a0a;
            }
            QLabel {
                color: #ddd;
                font-family: 'Consolas', monospace;
            }
            QLineEdit {
                background-color: #1a1a1a;
                color: #fff;
                border: 2px solid #333;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #00ff41;
            }
            QPushButton {
                background-color: #00ff41;
                color: #000;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: #00dd35;
            }
            QPushButton:pressed {
                background-color: #00bb29;
            }
            QTableWidget {
                background-color: #1a1a1a;
                color: #ddd;
                border: 2px solid #333;
                border-radius: 6px;
                gridline-color: #2a2a2a;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #00ff41;
                color: #000;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #00ff41;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QProgressBar {
                border: none;
                background-color: #1a1a1a;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #00ff41;
                border-radius: 4px;
            }
        """
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files_to_list(files)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            os.path.expanduser("~"),
            "All Files (*.*)"
        )
        if files:
            self.add_files_to_list(files)
    
    def add_files_to_list(self, files):
        for file_path in files:
            if os.path.isfile(file_path):
                if file_path in self.file_list:
                    continue
                
                self.file_list.append(file_path)
                
                mode = "DECRYPT" if file_path.lower().endswith('.png') else "ENCRYPT"
                
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                size_str = self._format_size(size)
                
                row = self.file_table.rowCount()
                self.file_table.insertRow(row)
                
                self.file_table.setItem(row, 0, QTableWidgetItem(filename))
                self.file_table.setItem(row, 1, QTableWidgetItem(size_str))
                self.file_table.setItem(row, 2, QTableWidgetItem(mode))
                
                status_item = QTableWidgetItem("Pending")
                status_item.setForeground(Qt.GlobalColor.yellow)
                self.file_table.setItem(row, 3, status_item)
    
    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def clear_list(self):
        self.file_list.clear()
        self.file_table.setRowCount(0)
        self.status_label.setText("")
    
    def process_files(self):
        if not self.file_list:
            QMessageBox.warning(self, "No Files", "Please add files to process.")
            return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "No Password", "Please enter an encryption password.")
            return
        
        self.btn_process.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.file_list))
        self.progress_bar.setValue(0)
        
        success_count = 0
        fail_count = 0
        
        for idx, file_path in enumerate(self.file_list):
            try:
                mode = "DECRYPT" if file_path.lower().endswith('.png') else "ENCRYPT"
                
                status_item = QTableWidgetItem("Processing...")
                status_item.setForeground(Qt.GlobalColor.cyan)
                self.file_table.setItem(idx, 3, status_item)
                self.status_label.setText(f"Processing: {os.path.basename(file_path)}")
                QApplication.processEvents()
                
                if mode == "ENCRYPT":
                    encrypted_bytes = self.crypto.encrypt_data(file_path, password)
                    cover_img = self.img_factory.generate_cover_image()
                    final_img = self.img_factory.embed_data(cover_img, encrypted_bytes)
                    
                    base_name = os.path.splitext(file_path)[0]
                    out_path = f"{base_name}_VAULT.png"
                    final_img.save(out_path)
                else:
                    encrypted_bytes = self.img_factory.extract_data(file_path)
                    plaintext, ext = self.crypto.decrypt_data(encrypted_bytes, password)
                    
                    base_name = file_path.replace("_VAULT", "").replace(".png", "")
                    out_path = f"{base_name}_RECOVERED{ext}"
                    
                    with open(out_path, 'wb') as f:
                        f.write(plaintext)
                
                status_item = QTableWidgetItem("Success")
                status_item.setForeground(Qt.GlobalColor.green)
                self.file_table.setItem(idx, 3, status_item)
                success_count += 1
                
            except Exception as e:
                status_item = QTableWidgetItem("Failed")
                status_item.setForeground(Qt.GlobalColor.red)
                self.file_table.setItem(idx, 3, status_item)
                fail_count += 1
            
            self.progress_bar.setValue(idx + 1)
            QApplication.processEvents()
        
        self.status_label.setText(f"{success_count} succeeded, {fail_count} failed")
        self.btn_process.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.information(
            self,
            "Processing Complete",
            f"Processed {len(self.file_list)} files\n\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}"
        )


def main():
    app = QApplication(sys.argv)
    
    # Handle command line argument for right-click integration
    if len(sys.argv) > 1:
        target_file = " ".join(sys.argv[1:]).strip().strip('"').strip("'")
        window = AetherVaultApp()
        if os.path.isfile(target_file):
            window.add_files_to_list([target_file])
    else:
        window = AetherVaultApp()
    
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
