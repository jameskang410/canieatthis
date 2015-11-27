from django.shortcuts import render
from django.shortcuts import render_to_response

from django.core.mail import send_mail

from django.http import JsonResponse

from elasticsearch import Elasticsearch
import redis

from textblob import TextBlob

def home(request):
	"""
	View for home
		-AJAX to get results
		-Sentiment analysis of results to get overall answer
	"""

	# get most recent searches from redis
	r = redis.StrictRedis()
	recent_search_array = r.lrange('recentsearches', 0, -1)

	# getting AJAX request
	if request.method == "POST":
		# user's input
		user_request = request.POST.get("food")

		es = Elasticsearch()

		# weighting search based on boost field
		# filtering out results with less than 0.5 scores
		search_query =  {
							'query' : {
								'function_score' : {
									'query' : {
										'match' : {
											'text' : user_request
										}
									},
									'min_score' : 0.5,
									'script_score' : {
										'script' : '_score * (float) _source.boost'
									}
								}
							}
						}

		data = es.search(index='pregnancy', doc_type='html', body=search_query)

		# array with all of the search hits
		hits_array = data['hits']

		# count of hits
		count = hits_array['total']

		# if there are any results
		if count > 0:

			# add formatted user_request to redis as the most recent search
			# removing everything but 5 most recent searches
			r.lpush('recentsearches', user_request.strip().lower())
			r.ltrim('recentsearches', 0, 4)

			# calculate avg sentiment analysis
			sentiment_sum = 0

			for hit in hits_array['hits']:

				# using TextBlob to get sentiment value of sentence
				sentence = hit['_source']['text']
				b = TextBlob(sentence)
				sentiment_num = b.sentiment[0]

				# adding sentiment value to sum
				sentiment_sum += sentiment_num

			# getting average
			sentiment_avg = sentiment_sum / count

			# based on sentiment avg, making conclusion
			# set threshold to 0.2
			if sentiment_avg >= 0.2:
				conclusion = "safe"
			else:
				conclusion = "not safe"


		# if no results - send e-mail with request
		else:
			conclusion = "na"

			email_message = 'The following food was searched but not found: <b>%s</b>' % user_request
			send_mail('REQUEST WAS ADDED', email_message, 'canieatthiswebsite@gmail.com', ['jameskang410@gmail.com'], html_message=email_message)

		return JsonResponse({"hits" : hits_array, "conclusion" : conclusion})


	return render(request, 'home/index.html', {"recent_searches" : recent_search_array})

def boost(request, increment_decrement, e_id):
	"""
	For "Was this helpful?" feature
	Receives elasticsearch ID and uses it to adjust boost 
	"""
	es = Elasticsearch()

	# figuring out if boost should be incremented or decremented
	if str(increment_decrement) == "yes":
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