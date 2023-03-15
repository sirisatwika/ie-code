import requests
import json
import base64
import hashlib
import hmac
import uuid
import OpenSSL
import datetime

# EdgeX Foundry API endpoint
api_endpoint = "https://localhost:8443"

# Credentials for authentication
credentials = {
    "username": "",
    "password": ""
}

# Generate a unique device ID
device_id = str(uuid.uuid4())

# Generate an x509 certificate for the device
key = OpenSSL.crypto.PKey()
key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
cert = OpenSSL.crypto.X509()
cert.get_subject().CN = device_id
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
cert.set_serial_number(1000)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, "sha256")

# Convert the certificate and private key to base64-encoded strings
cert_str = base64.b64encode(cert.to_cryptography().public_bytes(encoding=OpenSSL.crypto.FILETYPE_PEM)).decode("utf-8")
key_str = base64.b64encode(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)).decode("utf-8")

# Create a new device in EdgeX Foundry
device_data = {
    "name": device_id,
    "adminState": "UNLOCKED",
    "operatingState": "ENABLED",
    "protocols": {
        "custom": {
            "Settings": {
                "cert": cert_str,
                "key": key_str
            }
        }
    }
}
device_response = requests.post(f"{api_endpoint}/api/v2/device", json=device_data, auth=(credentials["username"], credentials["password"]))
if device_response.status_code != 201:
    print(f"Failed to create device: {device_response.status_code} {device_response.text}")
else:
    print(f"Created device {device_id}")
    
# Provision the device with EdgeX Foundry
provisioning_data = {
    "name": device_id,
    "identifiers": {
        "macAddress": ""
    },
    "profiles": [
        ""
    ],
    "labels": [
        ""
    ],
    "location": ""
}
provisioning_response = requests.post(f"{api_endpoint}/api/v2/provisionwatcher", json=provisioning_data, auth=(credentials["username"], credentials["password"]))
if provisioning_response.status_code != 201:
    print(f"Failed to provision device: {provisioning_response.status_code} {provisioning_response.text}")
else:
    print(f"Provisioned device {device_id}")