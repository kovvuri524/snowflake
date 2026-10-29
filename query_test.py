"""
Snowflake Metadata Retrieval Script

Purpose:
--------
Establishes a secure connection to Snowflake using RSA Key-Pair Authentication
and retrieves metadata about accessible databases and tables.

Responsibilities:
-----------------
1. Load environment variables from .env.
2. Read and process the RSA private key.
3. Authenticate with Snowflake using key-pair authentication.
4. Retrieve all accessible databases.
5. Count the number of tables in each database.
6. Display database and table count information.
7. Close Snowflake resources after execution.

Authentication:
---------------
Uses RSA Key-Pair Authentication (Public Key registered in Snowflake and
Private Key stored on the local machine).

Input:
------
- .env configuration file
- rsa_key.p8 (Private Key)

Output:
-------
- Total number of databases
- Database names
- Table counts for each database

Used For:
---------
- Snowflake connectivity validation
- Metadata retrieval
- Environment verification
- Authentication testing
"""

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
