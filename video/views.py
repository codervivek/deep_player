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
    for vi in video:
        if not (vi.json):
            headers = {
                # Request headers
                'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
            }

            params = urllib.parse.urlencode({
                # Request parameters
                'id': vi.embed,
            })

            try:
                conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
                conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/{id}?%s" % params, "", headers)
                response = conn.getresponse()
                string = response.read().decode('utf-8')
                json_obj = json.loads(string)
                print(json_obj)
                if(json_obj["state"]=="Processed"):
                    v=Video.objects.get(id=vi.id)
                    v.json=string
                    v.thumbnail=json_obj["summarizedInsights"]["thumbnailUrl"]
                    v.save()
                    # print(json_obj["summarizedInsights"]["thumbnailUrl"])
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))


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

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

class SearchListView(ListView):
    model = Video

    def get_queryset(self):
        qs = Video.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('json','name')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs

import json
from django.http import HttpResponse
# import 
def sceneSearch(request):
    qs = Video.objects.all()
    movie = request.GET.get('movie')
    m = 'abc'
    string = 'ab'
    if movie:
        query = SearchQuery(movie)
        vector=SearchVector('name')
        qs = qs.annotate(search=vector).filter(search=query)
        qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        m = qs[:1]
        q = request.GET.get('q')
        if not q:
            return render(request, 'scene.html', {'video':m[0]})
        print(m[0].name)
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'id': m[0].embed,
            'query': q,
            'pageSize': '1',
        })

        # try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params, "", headers)
        print("/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params)
        response = conn.getresponse()
        string = response.read().decode('utf-8')
        json_obj=json.loads(string)
        if(json_obj["results"][0]):
            string=json_obj["results"][0]["searchMatches"][0]["startTime"]
            timestr = string
            timestr = timestr.split('.')[0]
            ftr = [3600,60,1]
            string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
        print(string)
        conn.close()
        # except Exception as e:
        #     print("[Errno {0}] {1}".format(e.errno, e.strerror))
        # return render(request, 'video/video_detail.html', {'video': video})
        return render(request, 'scene.html', {'time':string,'video':m[0]})
        # return HttpResponse(json.dumps(json_obj), content_type="application/json")
        
    # else:
    #     m = qs
    #     headers = {
    #         # Request headers
    #         'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
    #     }

    #     params = urllib.parse.urlencode({
    #         # Request parameters
    #         'id': m[0].embed,
    #         'query': q,
    #         'pageSize': '1',
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
    #         conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params, "", headers)
    #         print("/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params)
    #         response = conn.getresponse()
    #         string = response.read().decode('utf-8')
    #         print(string)
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))


class VideoListView(ListView):
    model = Video