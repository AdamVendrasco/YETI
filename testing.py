from struct import unpack, pack
import io

def repair_jpeg(input_file, output_file):
    try:
        # Read the corrupted file
        with open(input_file, 'rb') as f:
            data = f.read()

        # Correct JPEG header and footer
        correct_header = b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        correct_footer = b'\xFF\xD9'

        # Check and fix the header
        if not data.startswith(correct_header):
            print("Fixing header...")
            data = correct_header + data[20:]  # Replace the first 20 bytes with the correct header

        # Identify the location of the footer
        footer_index = data.rfind(correct_footer)
        if footer_index == -1:
            print("Footer not found. Adding correct footer...")
            data += correct_footer  # Add the correct footer if missing
        else:
            # Truncate the file at the correct footer
            data = data[:footer_index + len(correct_footer)]

        # Look for and remove any junk data after the footer
        data_stream = io.BytesIO(data)
        repaired_data = bytearray()

        while True:
            marker = data_stream.read(2)
            if not marker or len(marker) < 2:
                break
            # If we find the footer marker, we stop processing further
            if marker == correct_footer:
                repaired_data.extend(marker)
                break
            # Read length of the segment and data
            length = unpack(">H", data_stream.read(2))[0] - 2
            repaired_data.extend(marker)
            repaired_data.extend(pack(">H", length + 2))
            repaired_data.extend(data_stream.read(length))

        # Save the repaired file
        with open(output_file, 'wb') as f:
            f.write(repaired_data)

        print("JPEG file has been repaired and saved as:", output_file)

    except Exception as e:
        print("An error occurred during repair:", e)

# Example usage
repair_jpeg('main/transmission.jpg', 'main/repaired_transmission.jpg')
