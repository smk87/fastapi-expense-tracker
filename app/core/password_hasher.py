from argon2 import PasswordHasher


def hash_password(password: str):
    ph = PasswordHasher()

    return ph.hash(password)


def verify_password(password: str, hashed_password: str):
    ph = PasswordHasher()

    try:
        ph.verify(hashed_password, password)

        return True

    except:
        return False
