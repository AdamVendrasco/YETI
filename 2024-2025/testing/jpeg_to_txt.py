import sys

def write_binary_to_hex_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'rb') as file:
            binary_data = file.read()
            hex_data = binary_data.hex()
            with open(output_file_path, 'w') as output_file:
                output_file.write(hex_data)
                print(f"Hex data written to {output_file_path}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_file_path>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        write_binary_to_hex_file(input_file, output_file)
