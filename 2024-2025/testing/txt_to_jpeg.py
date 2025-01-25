import sys

def hex_to_bin(hex_file, output_file):
    try:
        with open(hex_file, 'r') as f:
            hex_data = f.read().strip()
        byte_data = bytes.fromhex(hex_data)
        with open(output_file, 'wb') as f:
            f.write(byte_data)
            print(f"Binary data written to {output_file}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <hex_file> <output_file>")
    else:
        hex_file = sys.argv[1]
        output_file = sys.argv[2]
        hex_to_bin(hex_file, output_file)
