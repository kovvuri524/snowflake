# Snowflake Key-Pair Authentication Using Python

## Overview

This project demonstrates how to connect a local machine to Snowflake using RSA Key-Pair Authentication instead of a password.

The solution includes:

- RSA public/private key authentication
- Snowflake Python Connector
- Environment variable management using `.env`
- Metadata retrieval
- Database and table discovery

---

## Prerequisites

- Python 3.13+
- Snowflake Account
- OpenSSL (or Git Bash)
- Snowflake Connector for Python

---

## Setup

### Clone Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Create Virtual Environment

#### Windows

```powershell
py -3.13 -m venv venv313
.\venv313\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv313
source venv313/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Generate RSA Keys

### Generate Private Key

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

### Generate Public Key

```bash
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Generated files:

```text
rsa_key.p8
rsa_key.pub
```

---

## Configure Snowflake User

Open:

```text
rsa_key.pub
```

Remove:

```text
-----BEGIN PUBLIC KEY-----
-----END PUBLIC KEY-----
```

Convert the remaining key into a single line.

Run the following command in Snowflake:

```sql
ALTER USER <USERNAME>
SET RSA_PUBLIC_KEY='<PUBLIC_KEY>';
```

Verify:

```sql
DESC USER <USERNAME>;
```

---

## Configure Environment Variables

Create a `.env` file:

```env
SNOWFLAKE_USER=
SNOWFLAKE_ACCOUNT=
PRIVATE_KEY_PATH=rsa_key.p8
```

Example:

```env
SNOWFLAKE_USER=Gayatri09
SNOWFLAKE_ACCOUNT=xxxxxxxx
PRIVATE_KEY_PATH=rsa_key.p8
```

---

## Run the Application

### Test Snowflake Connection

```bash
python test_connection.py
```

### Get Database and Table Counts

```bash
python count_db_tables.py
```

---

## Example Output

```text
===== DATABASES =====

Total Databases: 6

Database: COMPANY | Tables: 2
Database: PRACTISE_DB | Tables: 1
Database: SNOWFLAKE | Tables: 0
Database: SNOWFLAKE_LEARNING_DB | Tables: 0
Database: SNOWFLAKE_SAMPLE_DATA | Tables: 80
Database: USER$GAYATRI09 | Tables: 0

```

## Project Structure

```text
snowflake/
│
├── requirements.txt
├── .env.example
├── .gitignore
│
├── test_connection.py
├── count_db_tables.py
├── key_connection.py
│
└── README.md
```

## Security Notes

Do not commit the following files to GitHub:

```text
.env
rsa_key.p8
rsa_key.pub
venv313/
```

Add the following entries to `.gitignore`:

```text
.env

venv313/

*.pem
*.p8
*.pub

__pycache__/
*.py*

```

# Authentication Flow
```
OpenSSL
    ↓
Generate RSA Key Pair
    ↓
Private Key (Stored on Local Machine)
Public Key (Registered in Snowflake)
    ↓
Python Uses Private Key
    ↓
Snowflake Validates Using Stored Public Key
    ↓
User Authentication Successful
    ↓
Connection Established
    ↓
Execute SQL Queries
    ↓
Retrieve Databases, Tables and Metadata
```