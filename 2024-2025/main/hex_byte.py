import os

# Define the function to fix the byte order. According to my jpg->txt script there is an issue 
# with the byte structure. 

def fix_jpeg_byte_order(input_file_path, output_file_path):
    # Opens the input file and read all binary data
    file = open(input_file_path, 'rb')
    binary_data = file.read()
    file.close()

    fixed_data = []
    # Iterates over the data in byte pairs
    for i in range(0, len(binary_data), 2):

        # Swaps the bytes manually and append to the fixed_data list
        first_byte = binary_data[i]
        second_byte = binary_data[i + 1]
        fixed_data.append(second_byte)
        fixed_data.append(first_byte)
    
    fixed_data_bytes = bytes(fixed_data)
    output_file = open(output_file_path, 'wb')
    output_file.write(fixed_data_bytes)
    output_file.close()
    
    #print(f"Fixed JPEG data written to {output_file_path}.")
    return fixed_data_bytes


# This function extracts multiple JPEGs inside the transmission.
def extract_jpegs(fixed_data_bytes, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Defines JPEG start and end markers. THis is standard SOis and EOIs according to wiki
    jpeg_start_marker = b'\xFF\xD8'
    jpeg_end_marker = b'\xFF\xD9'

    jpeg_images = []
    start_index = 0
    image_count = 0

    # Loops through the fixed data and look for JPEG markers
    while start_index < len(fixed_data_bytes):

        # Looks for the start of a new JPEG and breaks when the loop finds it.
        start_index = fixed_data_bytes.find(jpeg_start_marker, start_index)
        if start_index == -1:
            break 

        # Looks for the end of the JPEG and breaks when it findsit. 
        end_index = fixed_data_bytes.find(jpeg_end_marker, start_index)
        if end_index == -1:
            break 

        # This is to include the FF D9 footer EOI in the image
        end_index += 2

        # Extract the JPEG data
        jpeg_data = fixed_data_bytes[start_index:end_index]
        jpeg_images.append(jpeg_data)

        
        jpeg_file = open(f'{output_folder}/image_{image_count+1}.jpg', 'wb')
        jpeg_file.write(jpeg_data)
        jpeg_file.close()
        print(f"Extracted image {image_count+1}.jpg")
    
        start_index = end_index
        image_count += 1
    print(f"Extracted {image_count} images.")

#Saves all the new JPEGs
input_file = 'transmission.jpg'  
output_folder = 'extracted_images' 
fixed_data = fix_jpeg_byte_order(input_file, 'fixed_image_test.jpg')
extract_jpegs(fixed_data, output_folder)
