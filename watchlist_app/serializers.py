from dataclasses import fields
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['active']
    
    # custom serializers method
    def get_len_name(self, obj):
        return len(obj.name)
    
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
        