from django.shortcuts import render

# Create your views here.
from deep_player.forms import SignUpForm, UploadForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Video
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    video = Video.objects.annotate(
        max_created=Max("created_date")
    ).order_by("-max_created")
    return render(request, 'index.html', {'videos': video})

class VideoDetailView(generic.DetailView):
    model=Video

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
def fileupload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
            }
            n=form.cleaned_data.get('name')
            u=form.cleaned_data.get('url')
            user1=form.cleaned_data.get('user')
            params = urllib.parse.urlencode({
                # Request parameters
                'name': n,
                'privacy': 'Public',
                'videoUrl': u,
            })

            # try:
            conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
            conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?%s" % params, "", headers)
            response = conn.getresponse()
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
            user1=User.objects.get(id=user1)
            new_video = Video.objects.create(name=n,embed=json_obj,user=user1)
            new_video.save()
            # print(response.content)
            conn.close()
            return redirect('home')
            # except Exception as e:
            #     print("[Errno {0}] {1}".format(e.errno, e.strerror))
            #     return redirect('admin')
    else:
        form=UploadForm
    return render(request, 'upload.html',{'form':form})

def my_videos(request):
    video = Video.objects.annotate(
        max_created=Max("created_date")
    ).order_by("-max_created")
    return render(request, 'my_videos.html', {'videos': video})

def xyz(request):
    return render(request,'xyz.html')