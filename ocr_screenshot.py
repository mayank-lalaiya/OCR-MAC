#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import os
from PIL import Image
import pytesseract
from AppKit import NSPasteboard, NSPasteboardTypeString

# Set Tesseract path - try common locations
possible_paths = [
    '/opt/homebrew/bin/tesseract',  # Apple Silicon Macs
    '/usr/local/bin/tesseract',      # Intel Macs
    '/opt/local/bin/tesseract',      # MacPorts
]

tesseract_path = None
for path in possible_paths:
    if os.path.exists(path):
        tesseract_path = path
        break

# If not found in common locations, try to find it
if not tesseract_path:
    try:
        result = subprocess.run(['which', 'tesseract'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            tesseract_path = result.stdout.strip()
    except:
        pass

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"Using Tesseract at: {tesseract_path}")
else:
    print("ERROR: Tesseract not found!")
    print("Please install with: brew install tesseract")
    sys.exit(1)

def copy_to_clipboard(text):
    """Copy text to macOS clipboard"""
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.clearContents()
    pasteboard.setString_forType_(text, NSPasteboardTypeString)

def capture_screenshot():
    """Trigger macOS screenshot tool and return the image path"""
    # Create a temporary file for the screenshot
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    # Use macOS screencapture with interactive selection
    # -i: interactive mode (allows selection)
    # -s: selection mode only (no window capture)
    result = subprocess.run(['screencapture', '-i', temp_path], 
                          capture_output=True)
    
    # Check if user cancelled (file will be empty or very small)
    if os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:
        return temp_path
    else:
        # User cancelled, clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    try:
        image = Image.open(image_path)
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def main():
    # Step 1: Capture screenshot
    print("Select area to capture...")
    screenshot_path = capture_screenshot()
    
    if not screenshot_path:
        print("Screenshot cancelled")
        sys.exit(0)
    
    print(f"Screenshot saved to: {screenshot_path}")
    
    # Step 2: Extract text
    print("Extracting text...")
    extracted_text = extract_text_from_image(screenshot_path)
    
    # Step 3: Copy to clipboard
    if extracted_text:
        copy_to_clipboard(extracted_text)
        print("Text copied to clipboard!")
        print(f"\nExtracted text:\n{extracted_text}")
    else:
        print("No text found in the image")
    
    # Clean up temporary file
    os.remove(screenshot_path)

if __name__ == "__main__":
    main()
