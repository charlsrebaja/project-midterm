from rest_framework import serializers

class CipherRequestSerializer(serializers.Serializer):
    """Serializer for cipher request parameters"""
    text = serializers.CharField(required=True, help_text="Text to encrypt/decrypt")
    cipher_type = serializers.ChoiceField(
        choices=['atbash', 'caesar', 'vigenere'],
        default='caesar',
        help_text="Type of cipher to use"
    )
    mode = serializers.ChoiceField(
        choices=['encrypt', 'decrypt'],
        default='encrypt',
        help_text="Whether to encrypt or decrypt the text"
    )
    shift = serializers.IntegerField(required=False, default=3, help_text="Shift value for Caesar cipher")
    key = serializers.CharField(required=False, default='KEY', help_text="Key for Vigenere cipher")

class CipherResponseSerializer(serializers.Serializer):
    """Serializer for cipher response"""
    success = serializers.BooleanField()
    result = serializers.CharField(required=False)
    original = serializers.CharField(required=False)
    cipher_type = serializers.CharField(required=False)
    mode = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
