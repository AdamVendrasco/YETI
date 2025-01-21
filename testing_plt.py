from PIL import Image
import struct

def fix_jpeg(file_path, output_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Define the correct JPEG header and footer
    correct_header = b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    correct_footer = b'\xFF\xD9'

    # Check and replace header
    if not data.startswith(correct_header[:4]):  # Check first 4 bytes only
        print("Header is corrupted. Fixing...")
        data = correct_header + data[len(correct_header):]

    # Check and replace footer
    if not data.endswith(correct_footer):
        print("Footer is corrupted. Fixing...")
        data = data[:-2] + correct_footer  # Replace last 2 bytes with correct footer

    # Write the fixed data to a new file
    with open(output_path, 'wb') as f:
        f.write(data)

    # Attempt to open and re-save the image using Pillow
    try:
        with Image.open(output_path) as img:
            img.verify()  # Verify the image integrity
            img = Image.open(output_path)  # Re-open the image after verification
            img.save(output_path)  # Re-save to correct potential internal issues
        print("Image repaired and saved successfully.")
    except Exception as e:
        print("Failed to repair the image:", e)

# Example usage
fix_jpeg('main/transmission.jpg', 'main/repaired_transmission.jpg')
