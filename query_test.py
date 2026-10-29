from dotenv import load_dotenv
import os
import snowflake.connector
from cryptography.hazmat.primitives import serialization

load_dotenv()

# Load private key
with open(os.getenv("PRIVATE_KEY_PATH"), "rb") as key_file:
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

cur = conn.cursor()

print("\n===== DATABASES =====")

# Get all databases
cur.execute("SHOW DATABASES")

databases = cur.fetchall()

print(f"Total Databases: {len(databases)}")

for db in databases:
    database_name = db[1]  # name column

    query = f"""
    SELECT COUNT(*)
    FROM {database_name}.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE='BASE TABLE'
    """

    try:
        cur.execute(query)
        table_count = cur.fetchone()[0]

        print(
            f"Database: {database_name} | Tables: {table_count}"
        )

    except Exception:
        print(
            f"Database: {database_name} | Access Denied"
        )

cur.close()
conn.close()
