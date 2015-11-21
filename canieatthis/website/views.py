from django.shortcuts import render
from django.shortcuts import render_to_response

from rest_framework import generics
from website.serializers import FoodTableSerializer, UserTableSerializer

from website.models import FoodTable, UserTable

from django.core.mail import send_mail

from django.http import JsonResponse

from elasticsearch import Elasticsearch

from textblob import TextBlob

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
		user_request = request.POST.get("food")

		# format user's input - lower case (easier to put into database and for future queries)
		user_request = user_request.lower()

		# try finding first in database
		try:
			# doing a LIKE query (hopefully helps with misspellings)
			result = FoodTable.objects.get(food__contains=user_request)
			food = result.food
			source = result.source
			is_safe = result.can_eat
			text = "na"

		# else do text sentiment analysis via elasticsearch
		except:
			es = Elasticsearch()

			search_query =  {'query' : 
								{'term' : 
									{'text' : user_request}
								}
							}

			results = es.search(index='pregnancy', body=search_query)

			count = results['hits']['total']

			# found results
			if count > 0:
				# seems like hits are sorted by score so getting first one seems to be fine
				top_hit = results['hits']['hits'][0]

				hit_id = top_hit['_id']
				source = top_hit['_source']['source']
				text = top_hit['_source']['text']

				b = TextBlob(text)

				# sentiment - focusing on polarity expressed in a range from -1.0 - 1.0
				sentiment = b.sentiment[0]
				print(sentiment)
				if (sentiment >= 0.2):
					is_safe = "true"
				else:
					is_safe = "false"

			# could not find with elasticsearch
			else:
				is_safe = "unknown"
				source = "na"
				text = "na"

		return JsonResponse({"is_safe" : is_safe, "source" : source, "text" : text})


	return render(request, 'home/index.html')