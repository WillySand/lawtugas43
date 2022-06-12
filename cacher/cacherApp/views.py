from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mahasiswa
import requests
import json

@csrf_exempt
def update_mahasiswa(request):   
    if request.method == "POST":
        nama = request.POST['nama']
        npm = request.POST['npm']
        url = "https://law4update.herokuapp.com/"
        payload={'npm': npm}
        response = requests.request("POST", url=url, data=payload)
        return JsonResponse({'status':'OK'})
    return JsonResponse({'status': 'Method Not Allowed'})

@csrf_exempt
def reader_mahasiswa(request,npm):
    url = "https://law4read.herokuapp.com/"+npm
    response = requests.request("GET", url=url)
    
    return JsonResponse(json.loads(response.text))

@csrf_exempt
def reader_mahasiswa_cached(request,npm,trx_id):
    try:
        mahasiswa = Mahasiswa.objects.get(npm=npm)
        nama = mahasiswa.nama
        return JsonResponse({'status':'OK','npm':npm,'nama':nama})
    except :
        url = "https://law4read.herokuapp.com/"+npm
        response = requests.request("GET", url=url)
        try:
            nama = json.loads(response.text)['nama']
            mahasiswa = Mahasiswa(npm=npm, nama=nama)
            mahasiswa.save()
            return JsonResponse(json.loads(response.text))
        except:
            return JsonResponse(json.loads(response.text))
