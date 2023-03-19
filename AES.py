import os
import csv
import time
from Crypto.Cipher import AES

# Set the directory path
dir_path = './TestFiles'

# Set the AES encryption key (must be 16, 24, or 32 bytes long)
key = b'abcdefghijklmnop'

# Set the block size (must be 16 bytes)
block_size = 16

# Set the output file name and headers
output_file = 'AES_performance_analysis.csv'
headers = ['File Type', 'File Size', 'Encryption Time(ms)', 'Decryption Time(ms)']

# Create the output file and write the headers
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    # Iterate over the files in the directory
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)

        # Check if the file is a file (not a directory)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            file_type = os.path.splitext(filename)[1]

            # Read the file contents
            with open(filepath, 'rb') as f:
                file_contents = f.read()

            # Pad the file contents to the block size
            padding = block_size - len(file_contents) % block_size
            file_contents += bytes([padding]) * padding

            # Initialize the AES cipher
            cipher = AES.new(key, AES.MODE_CBC)

            # Encrypt the file contents and measure the encryption time
            start_time = time.time()
            encrypted_contents = cipher.encrypt(file_contents)
            encryption_time = (time.time() - start_time) * 1000

            # Initialize the AES cipher with the same key and IV
            cipher = AES.new(key, AES.MODE_CBC, iv=cipher.iv)

            # Decrypt the encrypted file contents and measure the decryption time
            start_time = time.time()
            decrypted_contents = cipher.decrypt(encrypted_contents)
            decryption_time = (time.time() - start_time) * 1000

            # Remove the padding from the decrypted file contents
            padding = decrypted_contents[-1]
            decrypted_contents = decrypted_contents[:-padding]

            # Write the results to the output file
            writer.writerow([file_type, file_size, encryption_time, decryption_time])
