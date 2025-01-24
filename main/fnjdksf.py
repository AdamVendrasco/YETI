import itertools

def read_file(filename):
    """Reads a file and returns its content as bytes."""
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, data):
    """Writes bytes data to a file."""
    with open(filename, 'wb') as f:
        f.write(data)

def find_jpeg_markers(data):
    """Checks if the data contains JPEG markers (SOI, APP0, EOI)."""
    markers = {
        'SOI': bytes.fromhex('FFD8'),  # Start of Image
        'APP0': bytes.fromhex('FFE0'),  # Start of Application Marker
        'EOI': bytes.fromhex('FFD9'),   # End of Image
    }
    
    found_markers = {marker_name: [] for marker_name in markers.keys()}
    
    # Search for marker positions
    for marker_name, marker in markers.items():
        position = data.find(marker)
        while position != -1:
            found_markers[marker_name].append(position)
            position = data.find(marker, position + 1)  # Look for next occurrence

    return found_markers

def reorder_chunks(data, chunk_size=2):
    """Splits data into chunks of specified size (default is 16-bit chunks)."""
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

def try_permutations(chunks):
    """Brute-force all permutations of chunks and validate each."""
    # Generate all permutations of the chunks
    for perm in itertools.permutations(chunks):
        perm_data = b''.join(perm)
        found_markers = find_jpeg_markers(perm_data)

        # Heuristic: Check if the order contains a valid SOI and EOI marker
        if found_markers['SOI'] and found_markers['EOI']:
            print(f"Valid permutation found: {found_markers}")
            # Save valid permutation to a new file
            write_file('reordered_valid_image.jpg', perm_data)
            return perm_data  # Return the valid reordered data

    return None  # No valid permutation found

def brute_force_reorder(filename):
    """Read file, brute-force chunk reordering, and apply heuristics."""
    # Step 1: Read the file
    data = read_file(filename)

    # Step 2: Reorder chunks (assuming 16-bit chunks)
    chunks = reorder_chunks(data, chunk_size=2)

    # Step 3: Try permutations of chunks and validate
    valid_data = try_permutations(chunks)

    if valid_data:
        print("Successfully found a valid permutation!")
    else:
        print("No valid permutation found.")

# Example usage:
filename = 'transmission.jpg'

brute_force_reorder(filename)
def extract_images_from_valid_data(data, soi_positions, eoi_positions, output_prefix="image"):
    """Extract valid JPEG images from data based on SOI and EOI markers."""
    images = []
    
    for i in range(len(soi_positions)):
        start_pos = soi_positions[i]
        
        # Find the next EOI marker after the current SOI marker (if any)
        end_pos = eoi_positions[i] if i < len(eoi_positions) else None
        
        if end_pos:
            image_data = data[start_pos:end_pos + 2]  # Include the EOI marker
            images.append(image_data)
            # Save the image to a new file
            output_filename = f"{output_prefix}_{i+1}.jpg"
            write_file(output_filename, image_data)
            print(f"Image {i+1} saved to {output_filename}")
    
    return images

# Example usage:
valid_data = read_file('reordered_valid_image.jpg')  # Read the valid reordered data
extract_images_from_valid_data(valid_data, [25439, 84915, 128116, 131339, 139177, 170404, 192270], 
                               [10312, 30636, 119454, 171454, 192268, 256001])
