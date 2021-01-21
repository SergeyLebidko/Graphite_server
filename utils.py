import random
import hashlib
from string import ascii_letters, digits


def to_hash(text):
    return hashlib.sha1(bytes(text, encoding='utf-8')).hexdigest()


def create_random_string(size):
    return ''.join([random.choice(ascii_letters + digits) for _ in range(size)])
