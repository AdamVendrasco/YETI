def swap_bytes_in_hex_file(input_file, output_file):
    # Open the input hex file in binary mode
    with open(input_file, 'rb') as file:
        # Read the entire file into memory
        data = file.read()
    # Ensure the file has at least 4 bytes to swap
    if len(data) < 4:
        raise ValueError("File is too small to swap bytes.")
    # Swap the first two bytes with the next two bytes
    swapped_data = data[2:4] + data[0:2] + data[4:]
    # Write the modified data to a new output file
    with open(output_file, 'wb') as file:
        file.write(swapped_data)
    print(f"Swapped bytes and saved to {output_file}")
# Example usage
input_file = 'main/transmission.jpg'  # Input JPEG file (hexadecimal format)
output_file = 'output.jpg'  # Output file with swapped bytes
swap_bytes_in_hex_file(input_file, output_file)








