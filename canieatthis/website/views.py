from django.shortcuts import render
from django.shortcuts import render_to_response

from rest_framework import generics
from website.models import FoodTable, UserTable
from website.serializers import FoodTableSerializer, UserTableSerializer

from django.core.mail import send_mail

from django.http import JsonResponse

"""
API logic
"""

class FoodList(generics.ListAPIView):
	"""
	Lists all food in approved DB
	Might want to take this out of production later
	"""

	queryset = FoodTable.objects.all()
	model = FoodTable
	serializer_class = FoodTableSerializer

class UserList(generics.ListAPIView):
	"""
	Lists all food in user (unapproved) DB
	Might want to take this out of production later
	"""

	queryset = UserTable.objects.all()
	model = UserTable
	serializer_class = UserTableSerializer

class AddFood(generics.CreateAPIView):
	"""
	Adding user-submitted food to unapproved DB
	"""

	# model = UserTable
	serializer_class = UserTableSerializer

"""
Actual views
"""
def home(request):
    """
    View for home
    """

    # getting AJAX request
    if request.method == "POST":
    	# user's input
    	food = request.POST.get("food")

    	return JsonResponse({"bool" : "true"})


    return render(request, 'home/index.html')