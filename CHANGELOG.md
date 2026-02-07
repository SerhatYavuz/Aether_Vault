# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2024-02-05

### Major Release - Complete Rewrite

#### Added
- Modern file list interface with QTableWidget
- Batch processing support for multiple files
- Drag and drop functionality
- Real-time progress tracking
- Enhanced UI with status indicators
- Offline mode with gradient image generation
- Automatic ZLIB compression
- Improved error handling and validation
- Right-click context menu integration
- Installation script for Linux

#### Changed
- Removed all API dependencies (fully offline capable)
- Simplified file naming convention (*_VAULT.png)
- Optimized encryption payload structure
- Improved 4K image generation with fallback
- Enhanced status messages and user feedback
- Upgraded security metadata version to 2.0

#### Removed
- HuggingFace API integration
- AI image generation dependencies
- Token management system
- Hardcoded file paths
- Unnecessary UI prompts

#### Fixed
- Hardcoded path issues for cross-platform compatibility
- Image display problems in right-click mode
- Capacity calculation edge cases
- File size format display
- UTF-8 encoding consistency

#### Security
- Maintained AES-256-GCM encryption
- Kept Argon2id key derivation parameters
- Added version field to detect future format changes

---

## [1.0.0] - 2024-01-15

### Initial Release

- Basic file encryption with AES-256
- LSB steganography implementation
- Simple PyQt6 GUI
- Command-line support
