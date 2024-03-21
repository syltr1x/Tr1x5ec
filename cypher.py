from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import os, random as r

def gen_key():
    return r.randint(100, 200)

def create_key(algoritmo, dato='', longitud=256, name=f"clave_{len(os.listdir('tray/'))}"):
    if algoritmo == 'RSA':
        key = RSA.generate(longitud)
        pub_key = key.publickey().export_key()
        priv_key = key.export_key()
        with open(f"tray/{name}.pub.pem", "wb") as f:
            f.write(pub_key)
        with open(f"tray/{name}.pri.pem", "wb") as f:
            f.write(priv_key)
        print("Claves RSA creadas correctamente.")
    elif algoritmo == 'AES':
        key = os.urandom(longitud // 8)
        with open(f"data/secrets/{name}_{dato}.bin", "wb") as f:
            f.write(key)
        print("Clave AES creada correctamente.")
    else:
        print("Algoritmo no válido.")

def get_key(tipo, algoritmo, name, dato):
    try: 
        if algoritmo == 'RSA':
            if tipo == 'pub': 
                with open(f'tray/{name}.pub.pem', 'rb') as pkp: 
                    key = RSA.import_key(pkp.read())
                pkp.close()
            else: 
                with open(f'tray/{name}.pri.pem', 'rb') as pkp:
                    key = RSA.import_key(pkp.read())
                pkp.close()
        elif algoritmo == 'AES':
            with open(f"data/secrets/{name}_{dato}.bin", "rb") as f:
                key = f.read()
    except FileNotFoundError:
        create_key(algoritmo, int(input("Tamaño para la clave. ej: 1024, 4096 >> ")))
        key = get_key(tipo, algoritmo)
    return key

def cifrar(algoritmo, clave, data, dato=''):
    key = get_key('pub', algoritmo, clave, dato)
    if algoritmo == 'RSA':
        data = data.encode()
        cipher_rsa = PKCS1_OAEP.new(key)
        ciphertext = cipher_rsa.encrypt(data)
        return ciphertext
    elif algoritmo == 'AES':
        with open(data, 'rb') as file:
            filepath = data
            data = file.read()
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length
        ciphertext = cipher.encrypt(data)
        with open(f'{filepath}', 'wb') as file_out:
            file_out.write(iv)  
            file_out.write(ciphertext)
        print("Archivo cifrado correctamente.")
    else:
        print("Algoritmo no válido.")
        return None
    
def descifrar(algoritmo, clave, data, dato=''):
    key = get_key('pri', algoritmo, clave, dato)
    if algoritmo == 'RSA':
        cipher_rsa = PKCS1_OAEP.new(key)
        plaintext = cipher_rsa.decrypt(data)
        return plaintext.decode()
    elif algoritmo == 'AES':
        with open(data, 'rb') as file:
            iv = file.read(16)
            ciphertext = file.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]
        with open(data, 'wb') as file_out:
            file_out.write(plaintext)
    else:
        print("Algoritmo no válido.")
        return None