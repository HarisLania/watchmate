from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, 
                                             write_only=True,
                                             style={'input_style': 'password'}
                                            )
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self, *args, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        if password != password2:
            raise serializers.ValidationError({'error': 'Password mismatch'})
        
        email = self.validated_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError({'error': 'User with email already exists'})
        
        user = User.objects.create(username=self.validated_data['username'], email=email)
        user.set_password(password)
        user.save()
        
        return user