from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import JsonResponse

from elasticsearch import Elasticsearch
import redis

from textblob import TextBlob

def home(request):
	"""
	View for home
		-bulk of it is AJAX to get results
		-Sentiment analysis of results to get overall answer
	"""

	# get most recent searches from redis
	r = redis.StrictRedis()
	recent_search_array = r.lrange('recent_searches', 0, -1)

	# getting AJAX request
	if request.method == "POST":
		# user's input
		user_request = request.POST.get("food")

		es = Elasticsearch()

		# weighting search based on boost field
		# filtering out results with less than 0.2 scores
		search_query =  {
							'query' : {
								'function_score' : {
									'query' : {
										'match' : {
											'text' : user_request
										}
									},
									'min_score' : 0.2,
									'script_score' : {
										'script' : '_score * (float) _source.boost'
									}
								}
							}
						}

		data = es.search(index='pregnancy', doc_type='html', body=search_query)

		# array with all of the search hits
		hits_array = data['hits']

		# get conclusion (safe/not safe/don't know) from sentiment analysis of results
		conclusion = sentiment_conclusion(hits_array)

		# if search term could not be found, add to redis list (that will be sent as e-mail)
		if conclusion == "na":
			r.lpush('missed_searches', user_request.strip().lower())

		# else search term was found, add formatted user_request to redis' recent searches
		else:
			r.lpush('recent_searches', user_request.strip().lower())
			# keeping only 5 most recent searches
			r.ltrim('recent_searches', 0, 4)

		return JsonResponse({"hits" : hits_array, "conclusion" : conclusion})

	return render(request, 'home/index.html', {"recent_searches" : recent_search_array})

def about(request):
	"""
	View for about page
	"""

	return render(request, 'about/about.html')

def boost(request):
	"""
	POST method for "Was this helpful?" feature
		-Receives info from custom URL and uses it to adjust boost field
		which affects scoring for subsequent searches
	"""
	# getting AJAX request
	if request.method == "POST":

		increment_decrement = request.POST.get("inc_dec_bool")
		e_id = request.POST.get("e_id")

		es = Elasticsearch()

		# figuring out if boost should be incremented or decremented
		if increment_decrement == "yes":
			operation = "+"
		else:
			operation = "-"

		# script written in groovy - adjusts boost and filters it to 0 - 2
		increment_script = 'ctx._source.boost %s= factor; if (ctx._source.boost < 0) \
		{ctx._source.boost = 0;} else if (ctx._source.boost > 2) { ctx._source.boost = 2; }' % operation
		
		# arbitrarily set to increase/decrease by factor of .1
		update_script = {
							'script' : {
								'inline' : increment_script,
								'params' : {
									'factor' : .1
								}
							}
						}

		response = es.update(index='pregnancy', id=e_id, doc_type='html', body=update_script)

		return JsonResponse(response)

def sentiment_conclusion(hits_array):
	"""
	Helper method for home view
		-Gets the avg sentiment from elasticsearch results and make a conclusion based on it (safe/not safe/don't know)
	"""
	# count of hits
	count = hits_array['total']

	# if there are any results
	if count > 0:

		# calculate avg sentiment analysis
		sentiment_sum = 0

		for hit in hits_array['hits']:

			# using TextBlob to get sentiment value of sentence
			sentence = hit['_source']['text']
			b = TextBlob(sentence)
			sentiment_num = b.sentiment[0]

			# adding sentiment value to sum
			sentiment_sum += sentiment_num

			# print(sentiment_num)

		# getting average
		sentiment_avg = sentiment_sum / count

		# print(sentiment_avg)

		# based on sentiment avg, making conclusion
		# set threshold to 0.1
		if sentiment_avg >= 0.1:
			conclusion = "safe"
		else:
			conclusion = "not safe"

	# if no results
	else:
		conclusion = "na"

	return conclusion