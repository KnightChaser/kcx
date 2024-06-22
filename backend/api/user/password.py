# password.py
# Utility functions for password hashing and verification

import bcrypt

# Hash the password
def password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

# Verify the password (returns True if the password is correct)
def password_verify(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))