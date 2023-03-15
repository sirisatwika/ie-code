import requests
import os
import json
import base64
import hashlib
import hmac
import uuid
import OpenSSL
import datetime
from cryptography import x509

def createX509():
    # Generate a unique CA ID
    ca_id = str(uuid.uuid4())
    
    # Generate an x509 CA certificate
    ca_key = OpenSSL.crypto.PKey()
    ca_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    ca_cert = OpenSSL.crypto.X509()
    ca_cert.get_subject().CN = ca_id
    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    ca_cert.set_serial_number(1000)
    ca_cert.set_issuer(ca_cert.get_subject())
    ca_cert.set_pubkey(ca_key)
    ca_cert.add_extensions([
        OpenSSL.crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
        OpenSSL.crypto.X509Extension(b"keyUsage", True, b"keyCertSign, cRLSign"),
        OpenSSL.crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert)
    ])
    ca_cert.sign(ca_key, "sha256")
    
    # Convert the CA certificate and private key to base64-encoded strings
    ca_cert_str = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert).decode("utf-8")
    ca_key_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, ca_key).decode("utf-8")

    CA_KEY_FILE = "ca_private.key"
    CA_CERT_FILE = "ca_cert.crt"
    
    #Load the CA cert and private key files
    with open(CA_CERT_FILE, "wt") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert).decode("utf-8"))
    with open(CA_KEY_FILE, "wt") as f:
        f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, ca_key).decode("utf-8"))
    
    # Generate a unique device ID
    device_id = str(uuid.uuid4())

    # Generate an x509 device certificate signed by the CA
    device_key = OpenSSL.crypto.PKey()
    device_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    device_cert = OpenSSL.crypto.X509()
    device_cert.get_subject().CN = device_id
    device_cert.gmtime_adj_notBefore(0)
    device_cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    device_cert.set_serial_number(1000)
    device_cert.set_issuer(ca_cert.get_subject())
    device_cert.set_pubkey(device_key)
    device_cert.add_extensions([
        OpenSSL.crypto.X509Extension(b"basicConstraints", True, b"CA:FALSE"),
        OpenSSL.crypto.X509Extension(b"keyUsage", True, b"digitalSignature, nonRepudiation, keyEncipherment"),
        OpenSSL.crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=device_cert),
        OpenSSL.crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid,issuer:always", issuer=ca_cert)
    ])
    device_cert.sign(ca_key, "sha256")
    
    # Convert the device certificate and private key to base64-encoded strings
    device_cert_str = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, device_cert).decode("utf-8")
    device_key_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, device_key).decode("utf-8")
    
    DEVICE_KEY_FILE = "device_private.key"
    DEVICE_CERT_FILE = "device_cert.crt"

    #Load the device cert and private key files
    with open(DEVICE_CERT_FILE, "wt") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, device_cert).decode("utf-8"))
    with open(DEVICE_KEY_FILE, "wt") as f:
        f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, device_key).decode("utf-8"))


def createSecretsDir(spath):
        path = spath
        
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        
        if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)