from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(read_only=True)
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    #object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("name and descriptions should be different")
        else:
            return data
    
    
    #field level validation
    def validate_name(self, name):
        if len(name) < 2:
            raise serializers.ValidationError("Name is too short")
        else:
            return name
        