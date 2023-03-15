from cryptography.fernet import Fernet
import base64

def createSymKey():
    # Generate a 256-bit symmetric key
    key = Fernet.generate_key()
    
    # Convert the key to a base64-encoded string
    encoded_key = base64.b64encode(key).decode('utf-8')
    
    print(f"Generated symmetric key: {encoded_key}")

    return encoded_key,201