import hashlib

from Crypto.Hash import SHA512


def custom_hash_md5(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()

def custom_hash_sha512(value: str) -> str:
    return SHA512.new(value.encode("utf-8")).hexdigest()

def custom_hash_sha512_obj(value: str) -> str:
    return SHA512.new(value.encode("utf-8"))