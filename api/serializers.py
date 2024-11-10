from rest_framework import serializers


class OpenAIRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)


