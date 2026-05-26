# Import hashlib for cryptographic hashing functions
import hashlib

def sha256_text(text: str) -> str:
    """
    Converts a text string to its SHA-256 hash representation.
    
    This function encodes the input text to UTF-8 bytes and computes
    the SHA-256 hash, returning it as a hexadecimal string.
    
    Args:
        text (str): The input text to hash
        
    Returns:
        str: The SHA-256 hash as a 64-character hexadecimal string
    """
    # Encode text to UTF-8 bytes (ignoring encoding errors) and compute SHA-256 hash
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def safe_decode_bytes(b: bytes) -> str:
    """
    Safely decodes bytes to a UTF-8 string with error handling.
    
    This function attempts to decode bytes to a string using UTF-8 encoding.
    If any decoding errors occur, they are ignored and replaced with
    the Unicode replacement character.
    
    Args:
        b (bytes): The bytes to decode
        
    Returns:
        str: The decoded string with any invalid characters replaced
    """
    # Decode bytes to UTF-8 string, ignoring any invalid byte sequences
    return b.decode("utf-8", errors="ignore")
