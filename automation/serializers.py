from rest_framework import serializers

class EmailTaskResponseSerializer(serializers.Serializer):
    """Serializer for email task response"""
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    result = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

class JokeAPIResponseSerializer(serializers.Serializer):
    """Serializer for joke API response"""
    success = serializers.BooleanField()
    joke = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
