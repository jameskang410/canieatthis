from rest_framework import serializers
from website.models import FoodTable, UserTable

class FoodTableSerializer(serializers.ModelSerializer):
	"""
	Approved model
	"""
	class Meta:
		model = FoodTable
		fields = ('food', 'can_eat')

class UserTableSerializer(serializers.ModelSerializer):
	"""
	User-submitted model
	"""
	class Meta:
		model = UserTable
		fields = ('food', 'can_eat')