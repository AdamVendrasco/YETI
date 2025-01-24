def fix_jpeg_byte_order(input_file_path, output_file_path):
    # Open the input file and read all binary data
    file = open(input_file_path, 'rb')
    binary_data = file.read()
    file.close()
    
    # Prepare a list to hold the fixed data
    fixed_data = []
    
    # Check if the file length is odd
    if len(binary_data) % 2 != 0:
        print("Warning: Odd number of bytes, last byte will be ignored.")
        binary_data = binary_data[:-1]  # Ignore the last byte
    
    # Iterate over the data in pairs
    for i in range(0, len(binary_data), 2):
        # Swap the bytes manually and append to the fixed_data list
        first_byte = binary_data[i]
        second_byte = binary_data[i + 1]
        fixed_data.append(second_byte)
        fixed_data.append(first_byte)
    
    # Convert the list back to bytes for writing
    fixed_data_bytes = bytes(fixed_data)
    
    # Write the fixed data to the output file
    output_file = open(output_file_path, 'wb')
    output_file.write(fixed_data_bytes)
    output_file.close()
    
    print(f"Fixed JPEG data written to {output_file_path}.")

# Example usage
input_file = 'transmission.jpg'
output_file = 'fixed.jpg'
fix_jpeg_byte_order(input_file, output_file)

