from dotenv import load_dotenv
import os

import snowflake.connector

from cryptography.hazmat.primitives import serialization

load_dotenv()

# Read private key
with open(
    os.getenv("PRIVATE_KEY_PATH"),
    "rb"
) as key_file:

    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

private_key = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    private_key=private_key
)

print("✅ Connected Successfully")

cur = conn.cursor()


cur.close()
conn.close()
