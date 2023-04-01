import os
import csv
import time
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

# Pad data
block_size = 8



# Define the directory path where the files are located
directory_path = './TestFiles'

# Define the key used for encryption and decryption
#key = '0123456789abcdef0123456789abcdef0123456789abcdef'.encode()
key = os.urandom(24)

# Define the CSV file path and column headers
csv_file_path = './3DES_performance.csv'
csv_columns = ['File Type', 'File Size', 'Encryption Time', 'Decryption Time']

# Initialize the list to store the data for CSV
csv_data = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    
    # Check if the path is a file and not a directory
    if os.path.isfile(file_path):
        # Get the file type and size
        file_type = os.path.splitext(filename)[1]
        file_size = os.path.getsize(file_path)
        
        # Read the file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
            padded_data = pad(file_content, block_size)
        # Perform encryption and measure the time
        start_time_encryption = time.time()
        cipher = DES3.new(key, DES3.MODE_ECB)
        encrypted_content = cipher.encrypt(padded_data)
        encryption_time = (time.time() - start_time_encryption)*1000
        
        # Perform decryption and measure the time
        start_time_decryption = time.time()
        decrypted_content = cipher.decrypt(encrypted_content)
        decryption_time = (time.time() - start_time_decryption)*1000
        
        # Check if the decrypted content matches the original content
        assert decrypted_content == padded_data, 'Decryption failed!'
        
        # Add the data to the CSV list
        csv_data.append({'File Type': file_type, 'File Size': file_size, 
                         'Encryption Time': encryption_time, 'Decryption Time': decryption_time})

# Write the CSV file
with open(csv_file_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for data in csv_data:
        writer.writerow(data)
