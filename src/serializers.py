from rest_framework import serializers
from src.models import QueryRequest

class QueryRequestSerializer(serializers.ModelSerializer):
    """Serializer for QueryRequest model."""

    class Meta:
        model = QueryRequest
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """Create a new QueryRequest instance."""
        return QueryRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing QueryRequest instance."""
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.question = validated_data.get("question", instance.question)
        instance.save()
        return instance