from rest_framework import serializers
from .models import Customer, LoyaltyProgram

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = ['points', 'tier', 'joined_date']

class CustomerSerializer(serializers.ModelSerializer):
    loyalty = LoyaltyProgramSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'customer_type', 'registration_date', 'birth_date',
            'address', 'is_active', 'loyalty'
        ]
        read_only_fields = ['id', 'registration_date']
    
    def validate_email(self, value):
        if Customer.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Клиент с таким email уже существует.")
        return value