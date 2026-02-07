# Contributing to AetherVault

Thank you for considering contributing to AetherVault.

## Code of Conduct

Please maintain a respectful and collaborative environment when contributing.

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Error messages or stack traces

### Suggesting Features

Feature suggestions are welcome. Please:
- Check existing issues first to avoid duplicates
- Clearly describe the proposed feature
- Explain the use case and benefits
- Consider security implications

### Pull Requests

1. Fork the repository
   ```bash
   git clone https://github.com/yourusername/aether-vault.git
   cd aether-vault
   ```

2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. Test thoroughly
   - Test encryption and decryption
   - Test edge cases
   - Verify UI remains responsive

5. Commit with clear messages
   ```bash
   git commit -m "Add: feature description"
   ```

6. Push and create pull request
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and concise

### Security

- Never weaken encryption algorithms
- Validate all user inputs
- Handle errors gracefully
- Avoid hardcoded credentials or paths

### Testing Checklist

Before submitting:
- [ ] Encryption produces valid output
- [ ] Decryption recovers original file
- [ ] Wrong password fails gracefully
- [ ] File size limits are enforced
- [ ] UI remains responsive during operations
- [ ] No crashes on edge cases
- [ ] Cross-platform compatibility verified

### Documentation

- Update README.md for new features
- Add entries to CHANGELOG.md
- Comment complex algorithms
- Update help text when needed

## Project Structure

```
aether-vault/
├── aether_vault.py      # Main application and UI
├── crypto_manager.py    # Encryption and decryption logic
├── image_factory.py     # Image generation and steganography
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── CHANGELOG.md        # Version history
└── install.sh          # Installation script
```

## Priority Areas

Current priorities for contributions:

### Performance
- Optimize image processing
- Improve multi-threading
- Reduce memory usage

### Features
- File integrity verification (checksums)
- Metadata wiping
- Secure file deletion
- Configuration file support

### Platform Support
- Windows compatibility testing
- macOS compatibility testing
- Additional Linux distributions

### UI Improvements
- Theme customization
- Keyboard shortcuts
- Better error messages
- Progress estimation

## Questions

If you have questions:
- Open an issue for discussion
- Check existing documentation
- Review closed issues for similar topics

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
