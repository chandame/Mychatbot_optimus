from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
#Create a chatbot
chatbot=ChatBot('jarvis')
trainer = ListTrainer(chatbot)

from django.conf import settings

file_ = open(os.path.join(settings.BASE_DIR, 'conversations.yml')).readlines()
#training on english dataset
#for files in os.listdir('./english/'):
#data=open('conversations.yml','r').readlines()
trainer.train(file_)

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)


def home(request):
	
	return render(request,'home.html')

def report(request):
	
	return render(request,'report.html')