from django.shortcuts import render
from .res.classifier import calculate_flare, testing
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

# This is the default view that handles the response
# to the base URL and when a POST request is made for
# predicting flair.

def index(request):
	data={}
	if request.method == "POST":
		print(request.POST['url'])
		data = calculate_flare(request.POST['url'])
		
	return render(request, 'index.html', {'data' : data})

# This view handles the automated testing part.
# For every POST request with a .txt file, this view 
# calculates flair and returns a json file.
@csrf_exempt
def automated_testing(request):

	str = request.body.decode('ASCII')
	str = str.split('\n')
	# str[3:-3] contains all the urls
	
	if request.method == "POST":
		json_file = testing(str[3:-3])
		print(json_file)
	return HttpResponse(json.dumps(json_file), content_type="application/json")