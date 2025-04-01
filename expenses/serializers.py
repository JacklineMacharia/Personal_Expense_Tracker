from rest_framework import serializers
from .models import Category, Expense
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Expense
        fields = ('id', 'user', 'category', 'category_id', 'amount', 'description', 'date', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at') 