from hashlib import sha512
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import rng as rng
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA3_256

generate = 0
private_key = 0
public_key = 0
fToEncrypt = 0
while 1:
    print()
    print('1 - Create new generator')
    print('2 - Generate new key pair')
    print('3 - Generate Signature')
    print('4 - Encrypt file')    
    print('5 - Decrypt file')
    print('6 - Exit')
    print()
    option = input("Choose option: ")

    if option == '1':
        try:
            generate = rng.RNG()
        except:
            print("Couldn't find file")
        else:
            print("Generated")
    elif option == '2' and generate:
        try:
            key = RSA.generate(1024, generate.getNextRandom)
            private_key = key.export_key()
            f_out = open("private_key.pem", "wb")
            f_out.write(private_key)
            f_out.close()
            public_key = key.publickey().export_key()
            f_out = open("public_key.pem", "wb")
            f_out.write(public_key)
            f_out.read
            f_out.close()
        except:
            print("Something went wrong")
        else:
            print("New keys generated")
    elif option == '3':
        hash = SHA3_256.new()

        with open("file.txt", 'rb') as file:
            chunk = 0

            while chunk != b'':
                chunk = file.read(1024)
                hash.update(chunk)

        key = RSA.import_key(open("private_key.pem").read())
        signature = pkcs1_15.new(key).sign(hash)

        with open("sign.txt", 'wb') as file:
            file.write(signature)

        print("Signature generated")
       
    elif option == '4':

        try:
            with open("file.txt", 'rb') as f:
                fData = f.read()
        except:
            print("Couldn't find file")
        else:
            f_out = open("file_encrypted.bin", "wb")
            recipient_key = RSA.import_key(open("public_key.pem").read())
            session_key = generate.getNextRandom(16)
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(fData)
            [f_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
            f_out.close()

            print("File encrypted as: file_encrypted.bin")

    elif option == '5':
        try:
            private_key = RSA.import_key(open('private_key.pem').read())
            f_in = open("file_encrypted.bin", "rb")
            enc_session_key, nonce, tag, ciphertext = \
                [f_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
            f_in.close()
        except:
            print(f"Wrong key, otherwise check if file path: file_encrypted.bin is valid")
        else:
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            f_out = open("decrypted_file.txt", "wb")
            f_out.write(data)
            f_out.close()
            print("File saved as decrypted_file.txt")

    elif option == '6':
        print()
        print("End of program")
        break
