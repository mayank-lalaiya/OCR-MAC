# OCR Screenshot Tool for Mac - Setup Guide

A simple OCR tool that captures screenshots and extracts text to your clipboard.

## Prerequisites

- macOS 10.13 or later
- Homebrew package manager
- Admin access to install software

## Installation Steps

### 1. Install Homebrew (if not already installed)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Required Dependencies

```bash
# Install Python 3 and Tesseract OCR
brew install python tesseract

# Verify installation
which tesseract
tesseract --version
```

### 3. Install Python Libraries

```bash
# Install required Python packages
pip3 install pytesseract pillow pyobjc-framework-Cocoa
```

### 4. Set Up the Script

```bash
# Create Scripts directory
mkdir -p ~/Scripts

# Copy ocr_screenshot.py to ~/Scripts/
# Make it executable
chmod +x ~/Scripts/ocr_screenshot.py

# Test the script
python3 ~/Scripts/ocr_screenshot.py
```

### 5. Create Shell Wrapper (Optional but Recommended)

Create `~/Scripts/run_ocr.sh`:

```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
cd ~/Scripts
python3 ocr_screenshot.py
```

Make it executable:

```bash
chmod +x ~/Scripts/run_ocr.sh
```

## Setting Up Keyboard Shortcut

### Option A: Using Automator (Built-in)

1. Open **Automator** (Cmd+Space, search "Automator")
2. Create **New Document** → **Quick Action**
3. Set "Workflow receives" to **no input** in **any application**
4. Search for and add **Run Shell Script** action
5. Paste the following code:
   ```bash
   ~/Scripts/run_ocr.sh
   ```
6. **File** → **Save** as "OCR Screenshot"
7. Go to **System Settings** → **Keyboard** → **Keyboard Shortcuts** → **Services**
8. Find "OCR Screenshot" under **General**
9. Click on it and assign your shortcut (e.g., **Cmd+Shift+6**)

**Note:** Cmd+Shift+5 is already used by macOS for screenshots.

### Option B: Using BetterTouchTool (Recommended)

1. Install [BetterTouchTool](https://folivora.ai/)
2. Open BetterTouchTool → **Keyboard** tab
3. Click **Add New Shortcut**
4. Set keyboard shortcut: **Cmd+Shift+6** (or your preference)
5. Choose action: **Execute Terminal Command (Async, in Background)**
6. Enter command: `~/Scripts/run_ocr.sh`

### Option C: Using Karabiner-Elements (Free)

1. Install [Karabiner-Elements](https://karabiner-elements.pqrs.org/)
2. Configure complex modifications to map your shortcut to run the script

## Grant Required Permissions

When you first run the tool, macOS will request permissions:

1. **Screen Recording Permission**
   - Go to **System Settings** → **Privacy & Security** → **Screen Recording**
   - Enable for Terminal (or Automator, depending on setup method)

2. **Accessibility Permission** (if prompted)
   - Go to **System Settings** → **Privacy & Security** → **Accessibility**
   - Enable for the appropriate app

## Usage

1. Press your configured keyboard shortcut (e.g., **Cmd+Shift+6**)
2. Click and drag to select the area containing text
3. Release to capture
4. Text is automatically extracted and copied to clipboard
5. Paste anywhere with **Cmd+V**

## Troubleshooting

### Tesseract Not Found Error

If you get "tesseract is not installed" error:

```bash
# Find Tesseract location
which tesseract

# If on Apple Silicon Mac, it should be:
# /opt/homebrew/bin/tesseract

# If on Intel Mac, it should be:
# /usr/local/bin/tesseract
```

The script automatically detects these paths. If it's installed elsewhere, the script will try to find it.

### Script Doesn't Run

Check permissions:

```bash
# Make sure script is executable
chmod +x ~/Scripts/ocr_screenshot.py
chmod +x ~/Scripts/run_ocr.sh

# Test directly
python3 ~/Scripts/ocr_screenshot.py
```

### Poor OCR Accuracy

For better recognition:

```bash
# Install additional language data
brew install tesseract-lang

# For specific languages (example: Hindi)
brew install tesseract-lang
```

Modify the script to specify language:
```python
text = pytesseract.image_to_string(image, lang='eng')  # or 'hin' for Hindi
```

### Keyboard Shortcut Not Working

- Check if another app is using the same shortcut
- Try a different key combination
- Make sure you've granted necessary permissions
- Restart the app/service after setup

## Uninstallation

```bash
# Remove the script
rm -rf ~/Scripts/ocr_screenshot.py ~/Scripts/run_ocr.sh

# Remove Python packages (optional)
pip3 uninstall pytesseract pillow pyobjc-framework-Cocoa

# Remove Tesseract (optional)
brew uninstall tesseract

# Remove Automator Quick Action
# Go to ~/Library/Services/ and delete "OCR Screenshot.workflow"
```

## Advanced Configuration

### Change OCR Language

Edit `ocr_screenshot.py` and modify the `extract_text_from_image` function:

```python
text = pytesseract.image_to_string(image, lang='eng+hin')  # Multiple languages
```

### Add Notification

Install `pync` for notifications:

```bash
pip3 install pync
```

Add to script:
```python
from pync import Notifier
Notifier.notify('Text copied to clipboard!', title='OCR Tool')
```

## Support

For issues or improvements, check:
- Tesseract documentation: https://github.com/tesseract-ocr/tesseract
- pytesseract documentation: https://pypi.org/project/pytesseract/

## Credits

- Tesseract OCR Engine by Google
- pytesseract Python wrapper
