import os
import time
import csv
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

directory = './TestFiles' # Replace with the directory path where the files are located
output_directory = './TestFiles_encdec' # Replace with the directory path where the encrypted and decrypted files will be stored
# valid_extensions = ['.txt', '.mp3', '.mp4', '.png'] # Replace with the list of valid extensions
valid_extensions = ['.mp4']
key = RSA.generate(2048)

with open('public_key.pem', 'wb') as f:
    f.write(key.publickey().export_key())

with open('private_key.pem', 'wb') as f:
    f.write(key.export_key())

public_key = RSA.import_key(open('public_key.pem').read())
private_key = RSA.import_key(open('private_key.pem').read())

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['File Type', 'File Size', 'Encryption Time', 'Decryption Time'])
    
    for file_name in os.listdir(directory):
        if os.path.splitext(file_name)[1] not in valid_extensions:
            continue
        
        file_path = os.path.join(directory, file_name)
        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(file_name)[1]
        
        with open(file_path, 'rb') as f_in:
            data = f_in.read()
            
            # Encrypt the data with AES
            aes_key = get_random_bytes(16)
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            
            # Encrypt the AES key with RSA
            cipher_rsa = PKCS1_OAEP.new(public_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            
            # Measure encryption time
            start_time = time.time()
            encrypted_data = encrypted_aes_key + cipher_aes.nonce + tag
            encryption_time = time.time() - start_time
            
            # Write encrypted data to file
            encrypted_file_path = os.path.join(output_directory, 'encrypted_' + file_name)
            with open(encrypted_file_path, 'wb') as f_out:
                f_out.write(encrypted_data)
            
            # Decrypt the data with AES
            nonce = encrypted_data[len(encrypted_aes_key):len(encrypted_aes_key)+16]
            tag = encrypted_data[len(encrypted_aes_key)+16:len(encrypted_aes_key)+32]
            ciphertext = encrypted_data[len(encrypted_aes_key)+32:]
            cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            
            # Measure decryption time
            start_time = time.time()
            decryption_time = time.time() - start_time
            
            # Write decrypted data to file
            decrypted_file_path = os.path.join(output_directory, 'decrypted_' + file_name)
            with open(decrypted_file_path, 'wb') as f_out:
                f_out.write(decrypted_data)
                
            # Write to CSV file
            writer.writerow([file_type, file_size, encryption_time, decryption_time])
