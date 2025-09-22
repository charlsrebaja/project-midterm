from rest_framework import serializers

class JokeRequestSerializer(serializers.Serializer):
    """Serializer for joke request parameters"""
    pass  # No parameters needed for joke fetch

class JokeResponseSerializer(serializers.Serializer):
    """Serializer for joke response"""
    success = serializers.BooleanField()
    joke = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    encrypted = serializers.DictField(required=False)
    qr_codes = serializers.DictField(required=False)
    error = serializers.CharField(required=False)
