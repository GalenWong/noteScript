from django.shortcuts import render

# Create your views here.
from .forms import UploadFileForm, uploadStringForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print(request.FILES['file'])
			data = {"stringshappy":"hey we got you"}
			return JsonResponse(data, safe = False)

		data = {"error":"not valid form"}
		return JsonResponse(data, safe = False)

	else:
		data = {"strings":"fuck you"}
		return JsonResponse(data, safe = False)


@csrf_exempt
def transcribe(request):
	if request.method == 'POST':
		form = uploadStringForm(request.POST, request.FILES)
		#j = json.loads(request.body)
		if form.is_valid:
			print(form)
			print(form['strToTranscribe'])
			data = form.cleaned_data
			string = data['strToTranscribe']
		data = {"transcribedStr": string}
		return JsonResponse(data, safe = False)