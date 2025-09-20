"""
Cipher utility functions for encryption and decryption
"""
import string


class CipherUtils:
    """Utility class for various cipher implementations"""
    
    @staticmethod
    def atbash_cipher(text, mode='encrypt'):
        """
        Atbash cipher: reverses the alphabet (A->Z, B->Y, etc.)
        Mode doesn't matter for Atbash as encryption = decryption
        """
        result = []
        
        for char in text:
            if char.upper() in string.ascii_uppercase:
                # Get position (0-25)
                pos = ord(char.upper()) - ord('A')
                # Reverse position
                new_pos = 25 - pos
                # Convert back to character
                new_char = chr(new_pos + ord('A'))
                # Preserve case
                if char.islower():
                    new_char = new_char.lower()
                result.append(new_char)
            else:
                # Keep non-alphabetic characters as is
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def caesar_cipher(text, shift=3, mode='encrypt'):
        """
        Caesar cipher: shifts each letter by a fixed number
        """
        if mode == 'decrypt':
            shift = -shift
        
        result = []
        
        for char in text:
            if char.upper() in string.ascii_uppercase:
                # Get ASCII value
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Shift character
                shifted = (ord(char) - ascii_offset + shift) % 26
                result.append(chr(shifted + ascii_offset))
            else:
                # Keep non-alphabetic characters as is
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def vigenere_cipher(text, key, mode='encrypt'):
        """
        Vigenere cipher: uses a repeating keyword to shift letters
        """
        if not key:
            return text
        
        # Clean the key (letters only, uppercase)
        key = ''.join(filter(str.isalpha, key.upper()))
        if not key:
            return text
        
        result = []
        key_index = 0
        
        for char in text:
            if char.upper() in string.ascii_uppercase:
                # Get shift from key
                shift = ord(key[key_index % len(key)]) - ord('A')
                
                if mode == 'decrypt':
                    shift = -shift
                
                # Apply shift
                ascii_offset = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - ascii_offset + shift) % 26
                result.append(chr(shifted + ascii_offset))
                
                # Move to next key character
                key_index += 1
            else:
                # Keep non-alphabetic characters as is
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def process_text(text, cipher_type, mode='encrypt', **kwargs):
        """
        Process text with specified cipher
        
        Args:
            text: Text to process
            cipher_type: 'atbash', 'caesar', or 'vigenere'
            mode: 'encrypt' or 'decrypt'
            **kwargs: Additional parameters (shift for Caesar, key for Vigenere)
        """
        if cipher_type == 'atbash':
            return CipherUtils.atbash_cipher(text, mode)
        elif cipher_type == 'caesar':
            shift = kwargs.get('shift', 3)
            return CipherUtils.caesar_cipher(text, shift, mode)
        elif cipher_type == 'vigenere':
            key = kwargs.get('key', 'KEY')
            return CipherUtils.vigenere_cipher(text, key, mode)
        else:
            raise ValueError(f"Unknown cipher type: {cipher_type}")
